import pytest

from statement_parser.utils.money import parse_naira_to_kobo


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1,000.00", 100_000),
        ("234,448.31", 23_444_831),
        ("486.09", 48_609),
        (".45", 45),
        ("6.00", 600),
        ("0.29", 29),
        ("0.00", 0),
        ("1,000", 100_000),
        (" 2,000.00 ", 200_000),
        ("-1,250.50", -125_050),
    ],
)
def test_parses_naira_text_to_kobo(text, expected):
    assert parse_naira_to_kobo(text) == expected


@pytest.mark.parametrize("text", [None, "", "   "])
def test_blank_cell_is_none(text):
    assert parse_naira_to_kobo(text) is None


@pytest.mark.parametrize("text", ["abc", "1.234", "12,34.00", "1,00.0.0", "-", "."])
def test_rejects_text_that_is_not_an_amount(text):
    with pytest.raises(ValueError):
        parse_naira_to_kobo(text)
