import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from statement_parser.data.models.base import Base, IdMixin, TimestampMixin
from statement_parser.data.models.enums.column import enum_column
from statement_parser.data.models.enums.statuses import FileType, JobSource, JobStatus


class Job(IdMixin, TimestampMixin, Base):
    __tablename__ = "jobs"
    __table_args__ = (
        UniqueConstraint("client_id", "idempotency_key"),
        Index("ix_jobs_client_file_hash", "client_id", "file_hash"),
    )

    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("api_clients.id"), index=True)
    client_user_id: Mapped[str] = mapped_column(String(100))
    input_source: Mapped[JobSource] = mapped_column(enum_column(JobSource))
    file_hash: Mapped[str | None] = mapped_column(String(64))
    file_type: Mapped[FileType | None] = mapped_column(enum_column(FileType))
    idempotency_key: Mapped[str] = mapped_column(String(100))
    status: Mapped[JobStatus] = mapped_column(
        enum_column(JobStatus), default=JobStatus.QUEUED, index=True
    )
    current_step: Mapped[str | None] = mapped_column(String(30))
    error_code: Mapped[str | None] = mapped_column(String(50))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    delete_after: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
