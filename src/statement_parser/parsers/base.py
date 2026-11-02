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
