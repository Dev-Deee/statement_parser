import uuid

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from statement_parser.data.models.base import Base, IdMixin, TimestampMixin


class Account(IdMixin, TimestampMixin, Base):
    __tablename__ = "accounts"
    __table_args__ = (
        UniqueConstraint("client_id", "account_fingerprint"),
        Index("ix_accounts_client_external_ref", "client_id", "external_ref"),
    )

    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("api_clients.id"))
    external_ref: Mapped[str] = mapped_column(String(100))
    bank_code: Mapped[str] = mapped_column(String(20))
    account_fingerprint: Mapped[str] = mapped_column(String(64))
    account_number_masked: Mapped[str] = mapped_column(String(20))
    account_name: Mapped[str | None] = mapped_column(String(200))
    currency: Mapped[str] = mapped_column(String(3), default="NGN")