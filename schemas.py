from pydantic import BaseModel
from datetime import date

class AuthorCreate(BaseModel):
    name: str
    bio: str

class AuthorResponse(AuthorCreate):
    model_config = {"from_attributes": True}

    id: int

class BookCreate(BaseModel):
    title: str
    summary: str
    publication_date: date
    author_id: int

class BookResponse(BookCreate):
    model_config = {"from_attributes": True}

    id: int
