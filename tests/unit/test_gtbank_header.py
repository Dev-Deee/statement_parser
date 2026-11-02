from datetime import date

import pytest

from statement_parser.parsers.gtbank import parse_header

HEADER_TEXT = """Customer Statement
DOE, JOHN ADE
Print Date:May 13, 2026 Address:1 FAKE STREET
Account No:0123456789 Currency:NGN
Period:May 4, 2026 \xad May 8, 2026 Opening Balance:253,347.19
Total Debit: 30,336.51 Closing Balance:226,610.68
Branch Name:SOMEWHERE Credit Count:3
Debit Count: 29 Total Credit: 3,600.00
Account Type:SASAV
"""


def test_reads_the_gtbank_header():
    summary = parse_header(HEADER_TEXT)

    assert summary.account_name == "DOE, JOHN ADE"
    assert summary.account_number == "0123456789"
    assert summary.currency == "NGN"
    assert summary.period_start == date(2026, 5, 4)
    assert summary.period_end == date(2026, 5, 8)
    assert summary.opening_balance_kobo == 25_334_719
    assert summary.closing_balance_kobo == 22_661_068
    assert summary.total_debit_kobo == 3_033_651
    assert summary.total_credit_kobo == 360_000
    assert summary.debit_count == 29
    assert summary.credit_count == 3


def test_missing_field_is_named_in_the_error():
    broken = HEADER_TEXT.replace("Opening Balance", "Opening Bal")
    with pytest.raises(ValueError, match="opening balance"):
        parse_header(broken)
