from sqlalchemy import Enum

def enum_column(enum_cls):
    return Enum(
        enum_cls,
        native_enum=False,
        length=20,
        values_callable=lambda e:[m.value for m in e],
    )