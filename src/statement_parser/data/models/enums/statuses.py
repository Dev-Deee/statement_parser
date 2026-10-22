from enum import StrEnum


class ClientStatus(StrEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"


class JobStatus(StrEnum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    NEEDS_REVIEW = "needs_review"
    FAILED = "failed"


class JobSource(StrEnum):
    UPLOAD = "upload"
    MONO = "mono"


class FileType(StrEnum):
    PDF = "pdf"
    CSV = "csv"
    XLSX = "xlsx"
