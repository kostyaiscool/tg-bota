#permission.py
from typing import List, TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from db.models.role import Role


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    roles: Mapped[List["Role"]] = relationship(
        secondary="role_permission",
        back_populates="permissions",
    )

    def __repr__(self) -> str:
        return f"<Permission(id={self.id}, name={self.name})>"