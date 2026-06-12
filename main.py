from typing import Annotated, Generator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/author/", response_model=list[schemas.Author])
def read_author(db: Annotated[Session, Depends(get_db)]):
    return crud.get_all_authors(db=db)


@app.post("/author/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Annotated[Session, Depends(get_db)]
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400, detail="Author with this name already exists"
        )

    return crud.create_author(
        db=db,
        author=author
    )


@app.get("/book/", response_model=list[schemas.Book])
def read_book(
    db: Annotated[Session, Depends(get_db)],
    author: str | None = None,
):
    return crud.get_book_list(
        db=db, authors=[author] if author else None
    )


@app.get("/book/{book_id}/", response_model=schemas.Book)
def read_single_book(
    book_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    db_book = crud.get_book_by_id(db=db, book_id=book_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.post("/book/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Annotated[Session, Depends(get_db)]
):
    db_book = crud.get_book_by_title(db=db, title=book.title)
    if db_book:
        raise HTTPException(status_code=400, detail="Book with this title already exists")

    author = crud.get_author_by_id(db=db, author_id=book.author_id)
    if not author:
        raise HTTPException(status_code=400, detail="Author not found")

    return crud.create_author(db=db, author=author)