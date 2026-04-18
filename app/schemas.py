from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field

# ---------- Book Schemas ----------

class BookBase(BaseModel):
    title: str
    summary: Optional[str] = None
    publication_date: date

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    author_id: int

    model_config = {"from_attributes": True}


# ---------- Author Schemas ----------

class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books: List[Book] = Field(default_factory=list)

    model_config = {"from_attributes": True}
