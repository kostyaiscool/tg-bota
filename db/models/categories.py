from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from db.base import Base


class Page(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(length=50), nullable=True)

    def __repr__(self) -> str:
        return f"<Page(id={self.id}, name={self.name}>"
