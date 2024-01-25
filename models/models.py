from sqlalchemy import MetaData, Table, Column, Integer, String, JSON, Boolean

metadata = MetaData()

message = Table(
    "message",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("message", JSON),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)
