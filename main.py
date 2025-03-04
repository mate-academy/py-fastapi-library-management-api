from typing import Annotated

from fastapi import FastAPI, Depends, Form
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import create_db_session

app = FastAPI()

class FilteredList:
    def __init__(
            self,
            model: type[models.Base],
    ) -> None:
        self.model = model

    def __call__(
            self,
            db_session: Session = Depends(create_db_session),
            skip: int | None = None,
            limit: int | None = None,

    ) -> list[type[models.Base]]:
        result = crud.get_list(
            db_session,
            self.model,
            skip=skip,
            limit=limit
        )
        return result


@app.post("/author/")
def create_author(
        item: Annotated[schemas.AuthorCreate, Form()],
        db_session: Session = Depends(create_db_session),
) -> None:
    crud.create(db_session, item)


@app.get("/author/", response_model=list[schemas.Author])
def get_authors(
        result: Annotated[list,
            Depends(FilteredList(models.Author))
        ]
) -> list:
    return [schemas.Author.model_validate(item) for item in result]


@app.get("/author/{author_id}", response_model=schemas.Author)
def get_author(
        author_id: int,
        db_session: Session = Depends(create_db_session),
) -> schemas.Author:
    result = crud.get_by_id(db_session, models.Author, author_id)
    return schemas.Author.model_validate(result)


@app.post("/book/")
def create_book(
        item: Annotated[schemas.BookCreate, Form()],
        db_session: Session = Depends(create_db_session),
) -> None:
    crud.create(db_session, item)


@app.get("/book/", response_model=list[schemas.Book])
def get_books(
        result: Annotated[
            list,
            Depends(FilteredList(models.Book))
        ]
) -> list:
    return [schemas.Book.model_validate(item) for item in result]


@app.get("/books/author/{author_id}", response_model=list[schemas.Book])
def get_books_by_author_id(
        author_id: int,
        db_session: Session = Depends(create_db_session),
) -> list[schemas.Book]:
    result = crud.get_books_by_author_id(db_session, author_id)
    return [schemas.Book.model_validate(item) for item in result]
