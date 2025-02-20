from pydantic import BaseModel, PastDatetime
class User(BaseModel):
    username: str
    reputation: str
    reg_date: PastDatetime
