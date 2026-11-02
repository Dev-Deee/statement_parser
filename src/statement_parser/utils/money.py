import re
from decimal import Decimal

# Optional minus, then either grouped thousands (1,000,000) or plain digits,
# then an optional decimal part of one or two digits.
_AMOUNT = re.compile(r"-?(\d{1,3}(,\d{3})*|\d+)?(\.\d{1,2})?")


def parse_naira_to_kobo(text: str | None) -> int | None:
    """Convert a naira amount as printed on a statement into kobo.

    Returns None for an empty cell. Raises ValueError for anything that
    is not a valid amount, rather than guessing.
    """
    if text is None:
        return None

    cleaned = text.strip()
    if not cleaned:
        return None

    has_digit = any(character.isdigit() for character in cleaned)
    if not has_digit or not _AMOUNT.fullmatch(cleaned):
        raise ValueError(f"Not a naira amount: {text!r}")

    amount = Decimal(cleaned.replace(",", ""))
    return int(amount * 100)
