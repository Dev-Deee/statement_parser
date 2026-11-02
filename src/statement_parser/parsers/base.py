from dataclasses import dataclass
from datetime import date

from statement_parser.data.models.enums.statuses import Channel, Direction


@dataclass(frozen=True)
class ParsedTransaction:
    """One transaction as read from a statement, before categorising or storing."""

    transaction_date: date
    value_date: date | None
    direction: Direction
    amount_kobo: int
    balance_after_kobo: int | None
    narration: str
    narration_truncated: bool
    bank_reference: str | None
    channel: Channel


@dataclass(frozen=True)
class StatementSummary:
    """The header of a statement: whose account, which period, and the bank's own totals."""

    account_name: str
    account_number: str
    currency: str
    period_start: date
    period_end: date
    opening_balance_kobo: int
    closing_balance_kobo: int
    total_debit_kobo: int | None = None
    total_credit_kobo: int | None = None
    debit_count: int | None = None
    credit_count: int | None = None


@dataclass(frozen=True)
class ParsedStatement:
    bank_code: str
    summary: StatementSummary
    transactions: tuple[ParsedTransaction, ...]
