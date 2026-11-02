import re

from statement_parser.data.models.enums.statuses import Channel, Direction
from statement_parser.parsers.base import ParsedTransaction
from statement_parser.utils.dates import parse_statement_date
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
