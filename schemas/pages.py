from pydantic import BaseModel, PastDatetime
class Pages(BaseModel):
    id: int
    name: str
    creation_date: PastDatetime
    text: str
    likes: int
    dislikes: int