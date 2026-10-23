from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from statement_parser.data.models.base import Base, IdMixin, TimestampMixin
from statement_parser.data.models.enums.column import enum_column
from statement_parser.data.models.enums.statuses import CategoryType, Channel


class Category(TimestampMixin, Base):
    __tablename__ = "categories"

    code: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    parent_code: Mapped[str | None] = mapped_column(ForeignKey("categories.code"))
    Category_type: Mapped[CategoryType] = mapped_column(enum_column(CategoryType))


class CategoryRule(IdMixin, TimestampMixin, Base):
    __tablename__ = "category_rules"

    pattern: Mapped[str] = mapped_column(String(200))
    channel: Mapped[Channel | None] = mapped_column(enum_column(Channel))
    bank_code: Mapped[str | None] = mapped_column(String(20))
    category_code: Mapped[str] = mapped_column(ForeignKey("categories.code"))
    priority: Mapped[int] = mapped_column(Integer, default=100)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
