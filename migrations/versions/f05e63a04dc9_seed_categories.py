"""seed categories

Revision ID: f05e63a04dc9
Revises: 9a8b7c6d5e4f
Create Date: 2026-10-23 23:48:42.983714

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f05e63a04dc9"
down_revision: str | Sequence[str] | None = "9a8b7c6d5e4f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# A lightweight copy of the table, frozen at this point in history.
categories = sa.table(
    "categories",
    sa.column("code", sa.String),
    sa.column("name", sa.String),
    sa.column("parent_code", sa.String),
    sa.column("category_type", sa.String),
)

PARENTS = [
    ("income", "Income", "income"),
    ("expense", "Expenses", "expense"),
    ("fee", "Bank fees", "fee"),
    ("transfer", "Transfers", "transfer"),
]

CHILDREN = [
    ("income.salary", "Salary", "income"),
    ("income.sales", "Sales", "income"),
    ("income.transfer_in", "Transfers received", "income"),
    ("income.refund", "Refunds", "income"),
    ("income.interest", "Interest", "income"),
    ("income.betting_winnings", "Betting winnings", "income"),
    ("income.other", "Other income", "income"),
    ("expense.food", "Food and eating out", "expense"),
    ("expense.groceries", "Groceries", "expense"),
    ("expense.airtime_data", "Airtime and data", "expense"),
    ("expense.electricity", "Electricity", "expense"),
    ("expense.rent", "Rent", "expense"),
    ("expense.transport", "Transport", "expense"),
    ("expense.fuel", "Fuel", "expense"),
    ("expense.shopping", "Shopping", "expense"),
    ("expense.health", "Health", "expense"),
    ("expense.education", "Education", "expense"),
    ("expense.entertainment", "Entertainment", "expense"),
    ("expense.subscriptions", "Subscriptions", "expense"),
    ("expense.supplier_payment", "Supplier payments", "expense"),
    ("expense.staff_salary", "Staff salaries", "expense"),
    ("expense.transfer_out", "Transfers sent", "expense"),
    ("expense.cash_withdrawal", "Cash withdrawals", "expense"),
    ("expense.loan_repayment", "Loan repayments", "expense"),
    ("expense.betting", "Betting", "expense"),
    ("expense.other", "Other expenses", "expense"),
    ("fee.bank_charge", "Bank charges", "fee"),
    ("fee.sms_alert", "SMS alert charges", "fee"),
    ("fee.vat", "VAT on charges", "fee"),
    ("fee.stamp_duty", "Stamp duty (EMTL)", "fee"),
    ("fee.card_maintenance", "Card maintenance", "fee"),
    ("transfer.internal", "Between own accounts", "transfer"),
    ("transfer.savings", "Savings and investments", "transfer"),
    ("transfer.loan_received", "Loans received", "transfer"),
]


def _codes(rows: Sequence[tuple[str, str, str]]) -> list[str]:
    return [code for code, _, _ in rows]


def upgrade() -> None:
    op.bulk_insert(
        categories,
        [
            {"code": code, "name": name, "parent_code": None, "category_type": kind}
            for code, name, kind in PARENTS
        ],
    )
    op.bulk_insert(
        categories,
        [
            {
                "code": code,
                "name": name,
                "parent_code": code.split(".")[0],
                "category_type": kind,
            }
            for code, name, kind in CHILDREN
        ],
    )


def downgrade() -> None:
    op.execute(categories.delete().where(categories.c.code.in_(_codes(CHILDREN))))
    op.execute(categories.delete().where(categories.c.code.in_(_codes(PARENTS))))
