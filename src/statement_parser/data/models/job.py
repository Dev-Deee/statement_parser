import uuid
from datetime import datetime

from sqlalchemy import UniqueConstraint, Index, ForeignKey, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from statement_parser.data.models.base import TimestampMixin, IdMixin, Base
from statement_parser.data.models.enums.column import enum_column
from statement_parser.data.models.enums.statuses import JobSource, FileType, JobStatus


class Job(IdMixin, TimestampMixin, Base):
    __tablename__ = "jobs"
    __table_args__ = (
        UniqueConstraint("client_id", "idempotency_key"),
        Index("ix_jobs_client_fie_hash", "client_id", "file_hash")
    )
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("api_clients.id"), index=True)
    external_reference: Mapped[str] = mapped_column(String(100))
    source: Mapped[str] = mapped_column(enum_column(JobSource))
    file_hash: Mapped[str | None] = mapped_column(String(64))
    file_type: Mapped[str | None] = mapped_column(enum_column(FileType))
    idempotency_key: Mapped[str] = mapped_column(String(100))
    status: Mapped[JobStatus] = mapped_column(
        enum_column(JobStatus), default=JobStatus.QUEUED, index=True
    )
    stage: Mapped[str | None] = mapped_column(String(30))
    error_code: Mapped[str | None] = mapped_column(String(50))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)