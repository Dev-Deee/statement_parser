from datetime import date, datetime

from statement_parser.utils.text import clean_cell


def parse_statement_date(text: str | None) -> date:
    """Parse dates like '04-May-2026', including GTBank's wrapped '04\\xadMay\\xad\\n2026'."""
    compact = clean_cell(text).replace(" ", "")
    try:
        return datetime.strptime(compact, "%d-%b-%Y").date()
    except ValueError as error:
        raise ValueError(f"Not a statement date: {text!r}") from error


def parse_long_date(text: str | None) -> date:
    """Parse header dates like 'May 4, 2026'."""
    cleaned = clean_cell(text)
    try:
        return datetime.strptime(cleaned, "%B %d, %Y").date()
    except ValueError as error:
        raise ValueError(f"Not a long date: {text!r}") from error
