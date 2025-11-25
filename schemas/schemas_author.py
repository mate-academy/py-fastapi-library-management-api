from pydantic import BaseModel


class BaseAuthor(BaseModel):
    name: str
    bio: str


class CreateAuthor(BaseAuthor):
    pass


class GetAuthor(BaseAuthor):
    id: int

    class Config:
        from_attributes = True