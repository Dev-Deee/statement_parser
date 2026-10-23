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


class Direction(StrEnum):
    CREDIT = "credit"
    DEBIT = "debit"


class ExtractionMethod(StrEnum):
    TEXT = "text"
    OCR = "ocr"
    MONO = "mono"


class BalanceCheckStatus(StrEnum):
    BALANCED = "balanced"
    MISMATCH = "mismatch"
    NOT_CHECKED = "not_checked"


class MismatchType(StrEnum):
    RUNNING_BALANCE = "running_balance"
    CLOSING_TOTAL = "closing_total"


class Channel(StrEnum):
    POS = "pos"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"
    USSD = "ussd"
    CARD = "card"
    AIRTIME = "airtime"
    BANK_CHARGE = "bank_charge"
    OTHER = "other"


class CategorisedBy(StrEnum):
    RULE = "rule"
    LLM = "llm"
    MANUAL = "manual"


class CategoryType(StrEnum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"
    FEE = "fee"
