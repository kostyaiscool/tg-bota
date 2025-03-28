from typing import Optional

from pydantic import BaseModel, PastDatetime
class TelegramUser(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    is_bot: bool
