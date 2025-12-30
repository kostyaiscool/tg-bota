from typing import Optional

from pydantic import BaseModel


class CommentaryCreate(BaseModel):
    id: int
    text: str
    author: int
    page: int