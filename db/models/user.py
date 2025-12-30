# user.py
from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import BigInteger, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base

if TYPE_CHECKING:
    from db.models.pages import Page
    from db.models.role import Role
    from db.models.commentaries import Commentary

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    username: Mapped[str | None] = mapped_column(String(32))
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str | None] = mapped_column(String(64))
    language_code: Mapped[str | None] = mapped_column(String(10))
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    is_bot: Mapped[bool] = mapped_column(Boolean, default=False)

    pages: Mapped[List["Page"]] = relationship(back_populates="author")

    roles: Mapped[List["Role"]] = relationship(
        secondary="user_role",
        back_populates="users",
        lazy="selectin",
    )

    commentaries: Mapped[list["Commentary"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)

