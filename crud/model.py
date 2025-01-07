from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pgvector.sqlalchemy import Vector


class Base(DeclarativeBase):
    pass


class Info(Base):
    __tablename__ = "info"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    embedding: Mapped[List[float]] = mapped_column(Vector)
