import uuid

from sqlalchemy import BigInteger, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from statement_parser.data.models.base import Base, IdMixin, TimestampMixin
from statement_parser.data.models.enums.column import enum_column
from statement_parser.data.models.enums.statuses import MismatchType


class BalanceMismatch(IdMixin, TimestampMixin, Base):
    __tablename__ = "balance_mismatches"
    statement_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("statements.id", ondelete="CASCADE"), index=True
    )
    mismatch_type: Mapped[int | None] = mapped_column(enum_column(MismatchType))
    row_index: Mapped[int | None] = mapped_column(Integer)
    expected_balance_kobo: Mapped[int] = mapped_column(BigInteger)
    actual_balance_kobo: Mapped[int] = mapped_column(BigInteger)
