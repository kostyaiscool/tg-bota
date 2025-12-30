from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.base import Base

if TYPE_CHECKING:
    from db.models.categories import Category
    from db.models.user import User
    from db.models import Page


class Commentary(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # title: Mapped[str] = mapped_column(String(length=50), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    creation_date: Mapped[str] = mapped_column(DateTime, default=datetime.now)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    author: Mapped["User"] = relationship(
        back_populates="commentaries"
    )

    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id"))
    page = relationship(
        "Page",
        back_populates="comments"
    )
    parent: Mapped[Optional["Commentary"]] = relationship("Commentary", remote_side=[id], backref="children")
    # likes: Mapped[int] = mapped_column(Integer, nullable=True)
    # dislikes: Mapped[int] = mapped_column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<Comment(id={self.id}, name={self.name}>"
