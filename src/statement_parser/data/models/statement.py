import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from statement_parser.data.models.base import Base, IdMixin, TimestampMixin
from statement_parser.data.models.enums.column import enum_column
from statement_parser.data.models.enums.statuses import BalanceCheckStatus, ExtractionMethod


class Statement(IdMixin, TimestampMixin, Base):
    __tablename__ = "statements"
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"), index=True)

    account_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"), index=True
    )

    period_start: Mapped[date] = mapped_column(Date)
    period_end: Mapped[date] = mapped_column(Date)
    opening_balance_kobo: Mapped[int] = mapped_column(BigInteger)
    closing_balance_kobo: Mapped[int] = mapped_column(BigInteger)
    transaction_count: Mapped[int] = mapped_column(Integer)
    statement_content_hash: Mapped[str] = mapped_column(String(64), index=True)
    extraction_method: Mapped[ExtractionMethod] = mapped_column(enum_column(ExtractionMethod))

    parser_version: Mapped[str] = mapped_column(String(20))
    balance_check_status: Mapped[BalanceCheckStatus] = mapped_column(
        enum_column(BalanceCheckStatus)
    )

    confidence_score: Mapped[Decimal] = mapped_column(Numeric(4, 3))
    delete_after: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
