from pydantic import BaseModel
from typing import List

class AuthorBase(BaseModel):
    name: str
    bio: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True