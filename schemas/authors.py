from pydantic import BaseModel


class AuthorCreateSchema(BaseModel):
    name: str
    bio: str


class AuthorResponseSchema(AuthorCreateSchema):
    id: int

    model_config = {"from_attributes": True}


class AuthorListSchema(BaseModel):
    authors: list[AuthorResponseSchema]

    model_config = {"from_attributes": True}
