from pydantic import BaseModel, PastDatetime

from schemas.categories import Categories
from schemas.user import TelegramUser


class Pages(BaseModel):
    id: int
    name: str
    creation_date: PastDatetime
    text: str
    likes: int
    dislikes: int
    categories: Categories
    author: TelegramUser

class PageCreate(BaseModel):
    name: str
    text: str
    category: Categories