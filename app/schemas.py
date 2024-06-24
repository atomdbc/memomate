from pydantic import BaseModel

class Entry(BaseModel):
    user_id: int
    content: str

    class Config:
        orm_mode = True
