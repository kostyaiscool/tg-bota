from pydantic import BaseModel


class Categories(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True