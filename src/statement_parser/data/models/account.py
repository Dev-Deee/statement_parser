import uuid

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from statement_parser.data.models.base import Base, IdMixin, TimestampMixin


class Account(IdMixin, TimestampMixin, Base):
    __tablename__ = "accounts"
    __table_args__ = (
        UniqueConstraint("client_id", "account_number_hash"),
        Index("ix_accounts_client_user_id", "client_id", "client_user_id"),
    )

    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("api_clients.id"))
    client_user_id: Mapped[str] = mapped_column(String(100))
    bank_code: Mapped[str] = mapped_column(String(20))
    account_number_hash: Mapped[str] = mapped_column(String(64))
    masked_account_number: Mapped[str] = mapped_column(String(20))
    account_name: Mapped[str | None] = mapped_column(String(200))
    currency: Mapped[str] = mapped_column(String(3), default="NGN")
