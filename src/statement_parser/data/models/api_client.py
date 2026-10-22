from sqlalchemy import LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from statement_parser.data.models.base import Base, IdMixin, TimestampMixin
from statement_parser.data.models.enums.column import enum_column
from statement_parser.data.models.enums.statuses import ClientStatus


class ApiClient(IdMixin, TimestampMixin, Base):
    __tablename__ = "api_clients"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    api_key_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    api_key_prefix: Mapped[str] = mapped_column(String(64))
    webhook_url: Mapped[str | None] = mapped_column(String(500))
    webhook_signing_secret_encrypted: Mapped[bytes | None] = mapped_column(LargeBinary)
    hashing_secret_encrypted: Mapped[bytes] = mapped_column(LargeBinary)
    status: Mapped[ClientStatus] = mapped_column(
        enum_column(ClientStatus), default=ClientStatus.ACTIVE
    )
