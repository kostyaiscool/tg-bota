# user.py
from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import BigInteger, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base

if TYPE_CHECKING:
    from db.models.pages import Page
    from db.models.role import Role

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
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    def has_role(self, role_name: str) -> bool:
        return any(role.name == role_name for role in self.roles)

    def has_permission(self, perm_name: str) -> bool:
        for role in self.roles:
            if any(permission.name == perm_name for permission in role.permission):
                return True
        return False