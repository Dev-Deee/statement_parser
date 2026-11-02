import pytest

from statement_parser.parsers.gtbank import select_transaction_rows

ROW_A = ["04\xadMay\xad\n2026", "'GTW", "04\xadMay\xad\n2026", "10.00", "", "100.00", "A"]
ROW_B = ["05\xadMay\xad\n2026", "'GTW", "05\xadMay\xad\n2026", "20.00", "", "80.00", "B"]
LAYOUT = [["Customer Statement\nDOE, JOHN", None, None], [None, "", ""]]


def test_table_repeated_on_every_page_is_read_once():
    tables = [LAYOUT, [ROW_A, ROW_B], LAYOUT, [ROW_A, ROW_B], LAYOUT, [ROW_A, ROW_B]]
    assert select_transaction_rows(tables) == [ROW_A, ROW_B]


def test_slices_across_pages_are_joined_in_order():
    assert select_transaction_rows([LAYOUT, [ROW_A], LAYOUT, [ROW_B]]) == [ROW_A, ROW_B]


def test_no_transaction_table_raises():
    with pytest.raises(ValueError):
        select_transaction_rows([LAYOUT])
