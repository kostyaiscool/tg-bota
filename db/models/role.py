from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, String, Boolean, DateTime, BigInteger, Table, Column, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.base import Base
if TYPE_CHECKING:
    from db.models.pages import Page

permission_role = Table(
    "permission_role", Base.metadata,
    Column("permission_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
          Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE")))

class Role(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(length=32), nullable=True)
    desc: Mapped[str] = mapped_column(String(64))
    permission: Mapped[List['Permission']] = relationship(back_populates='roles')

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name={self.name}, desc={self.desc})>"

class Permission(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(length=50), nullable=False)
    roles: Mapped[List['Role']] = relationship(back_populates='permission')