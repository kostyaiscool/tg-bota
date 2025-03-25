from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from db.base import Base


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    username: Mapped[str] = mapped_column(String(length=32), nullable=True)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)
    language_code: Mapped[str] = mapped_column(String(10), nullable=True)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    is_bot: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self) -> str:
        return f"<TelegramUser(id={self.id}, username={self.username}, is_premium={self.is_premium})>"