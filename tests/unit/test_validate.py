from datetime import date

from statement_parser.data.models.enums.statuses import Channel, Direction, MismatchType
from statement_parser.parsers.base import ParsedTransaction, StatementSummary
from statement_parser.pipeline.validate import BalanceIssue, check_statement


def make_summary(**overrides):
    values = {
        "account_name": "DOE, JOHN",
        "account_number": "0123456789",
        "currency": "NGN",
        "period_start": date(2026, 5, 4),
        "period_end": date(2026, 5, 8),
        "opening_balance_kobo": 10_000,
        "closing_balance_kobo": 8_500,
        "total_debit_kobo": 2_000,
        "total_credit_kobo": 500,
        "debit_count": 1,
        "credit_count": 1,
    }
    values.update(overrides)
    return StatementSummary(**values)


def make_transaction(direction, amount, balance):
    return ParsedTransaction(
        transaction_date=date(2026, 5, 4),
        value_date=None,
        direction=direction,
        amount_kobo=amount,
        balance_after_kobo=balance,
        narration="TEST",
        narration_truncated=False,
        bank_reference=None,
        channel=Channel.OTHER,
    )


DEBIT = make_transaction(Direction.DEBIT, 2_000, 8_000)
CREDIT = make_transaction(Direction.CREDIT, 500, 8_500)


def test_consistent_statement_has_no_issues():
    assert check_statement(make_summary(), [DEBIT, CREDIT]) == []


def test_wrong_running_balance_is_reported_at_its_row():
    wrong = make_transaction(Direction.CREDIT, 500, 8_600)

    issues = check_statement(make_summary(), [DEBIT, wrong])

    assert issues == [BalanceIssue(MismatchType.RUNNING_BALANCE, 1, 8_500, 8_600)]


def test_missing_row_is_caught():
    issues = check_statement(make_summary(), [DEBIT])
    found = {issue.mismatch_type for issue in issues}

    assert MismatchType.TRANSACTION_COUNT in found
    assert MismatchType.HEADER_TOTAL in found
    assert MismatchType.CLOSING_TOTAL in found


def test_duplicated_row_is_caught():
    assert check_statement(make_summary(), [DEBIT, DEBIT, CREDIT]) != []


def test_rows_without_balances_skip_the_running_check():
    rows = [
        make_transaction(Direction.DEBIT, 2_000, None),
        make_transaction(Direction.CREDIT, 500, None),
    ]
    assert check_statement(make_summary(), rows) == []
