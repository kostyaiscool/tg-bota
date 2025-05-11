from pydantic import BaseModel
class Categories(BaseModel):
    id: int
    name: str