# role.py
from typing import List, TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base

if TYPE_CHECKING:
    from db.models.user import User
    from db.models.permission import Permission

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    desc: Mapped[str | None] = mapped_column(String(128))

    users: Mapped[List["User"]] = relationship(
        secondary="user_role",  # посилання на таблицю з associations.py
        back_populates="roles",
    )

    permissions: Mapped[List["Permission"]] = relationship(
        secondary="role_permission",
        back_populates="roles",
    )

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name={self.name})>"