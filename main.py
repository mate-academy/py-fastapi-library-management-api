from typing import List

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root() -> dict:
    return {"message": "Server is up!"}


@app.get(
    "/authors/",
    response_model=list[schemas.Author],
)
def read_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
) -> List[schemas.Author]:
    return crud.get_authors_list(skip=skip, limit=limit, db=db)


@app.get(
    "/authors/{author_id}/",
    response_model=schemas.Author,
)
def read_author_by_id(
    author_id: int,
    db: Session = Depends(get_db),
) -> schemas.Author:
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail=f"Author with id {author_id} is not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
) -> schemas.Author:
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such name for Author already exists",
        )

    return crud.create_author(db=db, author=author)


@app.get(
    "/books/",
    response_model=list[schemas.Book],
)
def read_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    author_id: int | None = None,
    db: Session = Depends(get_db),
) -> List[schemas.Book]:
    return crud.get_book_list(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit,
    )


@app.post(
    "/books/",
    response_model=schemas.Book,
)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
) -> schemas.Book:
    return crud.create_book(db=db, book=book)
