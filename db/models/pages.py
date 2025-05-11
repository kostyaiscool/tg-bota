from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.base import Base
if TYPE_CHECKING:
    from db.models.categories import Category
    from db.models.user import User


class Page(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=50), nullable=True)
    creation_date: Mapped[str] = mapped_column(DateTime, default=datetime.now)
    text: Mapped[str] = mapped_column(Text)
    likes: Mapped[int] = mapped_column(Integer, nullable=True)
    dislikes: Mapped[int] = mapped_column(Integer, nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped['User'] = relationship(back_populates='pages')
    category_id: Mapped[int] = mapped_column(ForeignKey("categorys.id"))
    categories: Mapped['Category'] = relationship(back_populates='pages')

    def __repr__(self) -> str:
        return f"<Page(id={self.id}, name={self.name}>"
