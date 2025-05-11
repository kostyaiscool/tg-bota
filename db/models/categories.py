from typing import List

from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.base import Base
from db.models.pages import Page


class Category(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=50), nullable=True)
    pages: Mapped[List['Page']] = relationship(back_populates='categories')

    def __repr__(self) -> str:
        return f"<Page(id={self.id}, name={self.name}>"
