from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    pass


class AuthorList(AuthorBase):
    id: int

    class Config:
        orm_mode = True
