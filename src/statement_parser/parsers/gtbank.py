import re

from pdfplumber.pdf import PDF

from statement_parser.data.models.enums.statuses import Channel, Direction
from statement_parser.parsers.base import ParsedStatement, ParsedTransaction, StatementSummary
from statement_parser.utils.dates import parse_long_date, parse_statement_date
from statement_parser.utils.money import parse_naira_to_kobo
from statement_parser.utils.text import ELLIPSIS, clean_cell

COLUMN_COUNT = 7

# GTBank reference suffixes and what they mean.
REFERENCE_CHANNELS = {
    "AIR": Channel.AIRTIME,
    "NIP": Channel.TRANSFER_IN,
    "GTW": Channel.TRANSFER_OUT,
}

# Narrations that are bank charges, even when the reference says "transfer".
BANK_CHARGE_PATTERN = re.compile(r"SMS CHARGE|COMMISSION ON|VAT CHARGES", re.IGNORECASE)

# A reference only counts as a unique ID if it contains a long run of digits.
REAL_ID_PATTERN = re.compile(r"\d{8,}")


def _parse_reference(raw: str | None) -> tuple[str | None, Channel | None]:
    reference = clean_cell(raw).lstrip("'").strip()
    if not reference:
        return None, None

    channel = next(
        (ch for suffix, ch in REFERENCE_CHANNELS.items() if reference.endswith(suffix)),
        None,
    )
    is_real_id = not reference.endswith(ELLIPSIS) and REAL_ID_PATTERN.search(reference)
    return (reference if is_real_id else None), channel


def parse_row(row: list[str | None]) -> ParsedTransaction:
    """Turn one row of GTBank's transaction table into a ParsedTransaction."""
    if len(row) != COLUMN_COUNT:
        raise ValueError(f"Expected {COLUMN_COUNT} columns, got {len(row)}")

    trans_date, reference, value_date, debit, credit, balance, remarks = row

    debit_kobo = parse_naira_to_kobo(debit)
    credit_kobo = parse_naira_to_kobo(credit)
    if (debit_kobo is None) == (credit_kobo is None):
        raise ValueError("Row must have exactly one of debit or credit")

    if debit_kobo is not None:
        direction, amount = Direction.DEBIT, debit_kobo
    else:
        direction, amount = Direction.CREDIT, credit_kobo
    if amount <= 0:
        raise ValueError(f"Amount must be positive, got {amount}")

    narration = clean_cell(remarks)
    bank_reference, channel = _parse_reference(reference)
    if BANK_CHARGE_PATTERN.search(narration):
        channel = Channel.BANK_CHARGE

    return ParsedTransaction(
        transaction_date=parse_statement_date(trans_date),
        value_date=parse_statement_date(value_date) if clean_cell(value_date) else None,
        direction=direction,
        amount_kobo=amount,
        balance_after_kobo=parse_naira_to_kobo(balance),
        narration=narration,
        narration_truncated=ELLIPSIS in narration,
        bank_reference=bank_reference,
        channel=channel or Channel.OTHER,
    )


def parse_rows(rows: list[list[str | None]]) -> list[ParsedTransaction]:
    return [parse_row(row) for row in rows]


BANK_CODE = "gtbank"


def _find(pattern: str, text: str, field: str) -> re.Match[str]:
    match = re.search(pattern, text)
    if match is None:
        raise ValueError(f"GTBank header: could not find {field}")
    return match


def _amount(pattern: str, text: str, field: str) -> int:
    value = parse_naira_to_kobo(_find(pattern, text, field).group(1))
    if value is None:
        raise ValueError(f"GTBank header: {field} is empty")
    return value


def parse_header(text: str) -> StatementSummary:
    """Read the statement header from the first page's text."""
    period = _find(
        r"Period:\s*([A-Za-z]+ \d{1,2}, \d{4})\W+([A-Za-z]+ \d{1,2}, \d{4})", text, "period"
    )
    return StatementSummary(
        account_name=_find(r"Customer Statement\s*\n\s*(.+?)\s*\n", text, "account name").group(1),
        account_number=_find(r"Account No:\s*(\d{10})", text, "account number").group(1),
        currency=_find(r"Currency:\s*([A-Z]{3})", text, "currency").group(1),
        period_start=parse_long_date(period.group(1)),
        period_end=parse_long_date(period.group(2)),
        opening_balance_kobo=_amount(r"Opening Balance:\s*(\S+)", text, "opening balance"),
        closing_balance_kobo=_amount(r"Closing Balance:\s*(\S+)", text, "closing balance"),
        total_debit_kobo=_amount(r"Total Debit:\s*(\S+)", text, "total debit"),
        total_credit_kobo=_amount(r"Total Credit:\s*(\S+)", text, "total credit"),
        debit_count=int(_find(r"Debit Count:\s*(\d+)", text, "debit count").group(1)),
        credit_count=int(_find(r"Credit Count:\s*(\d+)", text, "credit count").group(1)),
    )


def _is_transaction_table(table: list[list[str | None]]) -> bool:
    if not table or len(table[0]) != COLUMN_COUNT:
        return False
    try:
        parse_statement_date(table[0][0])
    except ValueError:
        return False
    return True


def select_transaction_rows(tables: list[list[list[str | None]]]) -> list[list[str | None]]:
    """Collect transaction rows across pages, using each distinct table once.

    GTBank repeats the whole table on every page, so identical copies are
    skipped. If a statement ever splits rows across pages, the distinct
    slices are joined in page order. Validation checks the result either way.
    """
    distinct: list[list[list[str | None]]] = []
    for table in tables:
        if _is_transaction_table(table) and table not in distinct:
            distinct.append(table)

    if not distinct:
        raise ValueError("No GTBank transaction table found")
    return [row for table in distinct for row in table]


def parse_pdf(pdf: PDF) -> ParsedStatement:
    """Parse an open GTBank statement PDF."""
    summary = parse_header(pdf.pages[0].extract_text() or "")
    tables = [table for page in pdf.pages for table in page.extract_tables()]
    transactions = tuple(parse_rows(select_transaction_rows(tables)))
    return ParsedStatement(bank_code=BANK_CODE, summary=summary, transactions=transactions)
