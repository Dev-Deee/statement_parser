from datetime import date

import pytest

from statement_parser.utils.dates import parse_statement_date


@pytest.mark.parametrize("text", ["04-May-2026", "04\xadMay\xad\n2026"])
def test_parses_gtbank_dates(text):
    assert parse_statement_date(text) == date(2026, 5, 4)


@pytest.mark.parametrize("text", [None, "", "May 4 2026", "32-May-2026"])
def test_rejects_invalid_dates(text):
    with pytest.raises(ValueError):
        parse_statement_date(text)
