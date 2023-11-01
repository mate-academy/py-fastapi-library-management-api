from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorType(AuthorBase):  # list
    id: int

    class Config:
        orm_mode = True
