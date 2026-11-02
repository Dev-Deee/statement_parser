from collections.abc import Sequence
from dataclasses import dataclass

from statement_parser.data.models.enums.statuses import Direction, MismatchType
from statement_parser.parsers.base import ParsedTransaction, StatementSummary


@dataclass(frozen=True)
class BalanceIssue:
    mismatch_type: MismatchType
    row_index: int | None
    expected: int
    actual: int


def check_statement(
    summary: StatementSummary, transactions: Sequence[ParsedTransaction]
) -> list[BalanceIssue]:
    """Check a parsed statement against the bank's own numbers.

    An empty list means every check passed.
    """
    issues: list[BalanceIssue] = []
    debits = [t for t in transactions if t.direction is Direction.DEBIT]
    credits = [t for t in transactions if t.direction is Direction.CREDIT]
    debit_sum = sum(t.amount_kobo for t in debits)
    credit_sum = sum(t.amount_kobo for t in credits)

    # 1. Row counts against the header.
    for expected, actual in (
        (summary.debit_count, len(debits)),
        (summary.credit_count, len(credits)),
    ):
        if expected is not None and expected != actual:
            issues.append(BalanceIssue(MismatchType.TRANSACTION_COUNT, None, expected, actual))

    # 2. Totals against the header.
    for expected, actual in (
        (summary.total_debit_kobo, debit_sum),
        (summary.total_credit_kobo, credit_sum),
    ):
        if expected is not None and expected != actual:
            issues.append(BalanceIssue(MismatchType.HEADER_TOTAL, None, expected, actual))

    # 3. Each running balance must follow from the one before.
    previous: int | None = summary.opening_balance_kobo
    for index, transaction in enumerate(transactions):
        if transaction.balance_after_kobo is None:
            previous = None
            continue
        if previous is not None:
            change = transaction.amount_kobo
            if transaction.direction is Direction.DEBIT:
                change = -change
            expected_balance = previous + change
            if transaction.balance_after_kobo != expected_balance:
                issues.append(
                    BalanceIssue(
                        MismatchType.RUNNING_BALANCE,
                        index,
                        expected_balance,
                        transaction.balance_after_kobo,
                    )
                )
        previous = transaction.balance_after_kobo

    # 4. Opening + credits - debits must equal closing.
    computed_closing = summary.opening_balance_kobo + credit_sum - debit_sum
    if computed_closing != summary.closing_balance_kobo:
        issues.append(
            BalanceIssue(
                MismatchType.CLOSING_TOTAL, None, summary.closing_balance_kobo, computed_closing
            )
        )

    return issues
