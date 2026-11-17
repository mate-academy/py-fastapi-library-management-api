from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud import (
    create_author,
    list_of_authors,
    get_author_by_id,
    create_book,
    list_of_books,
    get_author_by_name,
)
from database import SessionLocal, Base, engine
from schemas import AuthorRead, AuthorCreate, BookRead, BookCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    with SessionLocal() as db_session:
        yield db_session


SessionDepends = Annotated[Session, Depends(get_db)]


@app.post(
    "/authors/",
    response_model=AuthorRead,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"description": "Author with this name already exists"}},
)
def create_new_author(db: SessionDepends, author_data: AuthorCreate):
    author = get_author_by_name(db=db, name=author_data.name)
    if author:
        raise HTTPException(
            status_code=400, detail="Author with this name already exists"
        )

    return create_author(db=db, author_data=author_data)


@app.get(
    "/authors/",
    response_model=list[AuthorRead],
    responses={400: {"description": "Invalid pagination parameters"}},
)
def get_all_authors(db: SessionDepends, skip: int = 0, limit: int = 100):
    if limit > 100 or limit < 0:
        raise HTTPException(
            status_code=400, detail="Limit must be in range from 0 to 100"
        )
    elif skip < 0:
        raise HTTPException(status_code=400, detail="Skip must be >= 0")

    return list_of_authors(db=db, skip=skip, limit=limit)


@app.get(
    "/authors/{author_id}",
    response_model=AuthorRead,
    responses={404: {"description": "Author not found"}},
)
def get_author(db: SessionDepends, author_id: int):
    author = get_author_by_id(db=db, author_id=author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@app.post(
    "/books/",
    response_model=BookRead,
    status_code=status.HTTP_201_CREATED,
    responses={404: {"description": "Author was not found"}},
)
def create_new_book(db: SessionDepends, book_data: BookCreate):
    author = get_author_by_id(db=db, author_id=book_data.author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author was not found")

    return create_book(db=db, book_data=book_data)


@app.get(
    "/books/",
    response_model=list[BookRead],
    responses={
        400: {"description": "Invalid pagination parameters"},
    },
)
def get_all_books(
    db: SessionDepends, author_id: int | None = None, skip: int = 0, limit: int = 100
):
    if limit > 100 or limit < 0:
        raise HTTPException(
            status_code=400, detail="Limit must be in range from 0 to 100"
        )
    elif skip < 0:
        raise HTTPException(status_code=400, detail="Skip must be >= 0")

    return list_of_books(db=db, author_id=author_id, skip=skip, limit=limit)
