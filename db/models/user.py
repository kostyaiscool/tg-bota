from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, String, Boolean, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.base import Base
if TYPE_CHECKING:
    from db.models.pages import Page


class User(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    username: Mapped[str] = mapped_column(String(length=32), nullable=True)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)
    language_code: Mapped[str] = mapped_column(String(10), nullable=True)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    is_bot: Mapped[bool] = mapped_column(Boolean, default=False)
    pages: Mapped[List['Page']] = relationship(back_populates='author')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    roles: Mapped['Role'] = relationship(back_populates='users')

    def __repr__(self) -> str:
        return f"<TelegramUser(id={self.id}, username={self.username}, is_premium={self.is_premium})>"