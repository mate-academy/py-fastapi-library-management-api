from pydantic import BaseModel, ConfigDict

class BaseAuthor(BaseModel):
    name: str
    bio: str

class AuthorCreate(BaseAuthor):
    pass

class Author(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)

class BaseBook(BaseModel):
    title: str
    author: Author
    summary: str

class BookCreate(BaseBook):
    pass

class Book(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)
