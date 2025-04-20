from pydantic import BaseModel
from typing import Optional


class TelegramUser(BaseModel):
    id: int
    username: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    is_bot: bool
