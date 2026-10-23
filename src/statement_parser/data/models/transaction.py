import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from statement_parser.data.models.base import Base, IdMixin, TimestampMixin
from statement_parser.data.models.enums.column import enum_column
from statement_parser.data.models.enums.statuses import CategorisedBy, Channel, Direction


class Transaction(IdMixin, TimestampMixin, Base):
    __tablename__ = "transactions"
    __table_args__ = (
        UniqueConstraint("account_id", "duplicate_check_hash"),
        Index("ix_transactions_account_date", "account_id", "transaction_date"),
        CheckConstraint("amount_kobo > 0", name="amount_positive"),
    )

    account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))
    first_seen_in_statement_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("statements.id", ondelete="SET NULL")
    )
    transaction_date: Mapped[date] = mapped_column(Date)
    value_date: Mapped[date | None] = mapped_column(Date)
    direction: Mapped[Direction] = mapped_column(enum_column(Direction))
    amount_kobo: Mapped[int] = mapped_column(BigInteger)
    balance_after_kobo: Mapped[int | None] = mapped_column(BigInteger)
    narration: Mapped[str] = mapped_column(Text)
    narration_truncated: Mapped[bool] = mapped_column(Boolean, default=False)
    bank_reference: Mapped[str | None] = mapped_column(String(64))
    channel: Mapped[Channel | None] = mapped_column(enum_column(Channel))
    counterparty_name: Mapped[str | None] = mapped_column(String(200))
    category_code: Mapped[str | None] = mapped_column(ForeignKey("categories.code"))
    categorised_by: Mapped[CategorisedBy | None] = mapped_column(enum_column(CategorisedBy))
    category_confidence: Mapped[Decimal | None] = mapped_column(Numeric(4, 3))
    duplicate_check_hash: Mapped[str] = mapped_column(String(64))
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    delete_after: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
