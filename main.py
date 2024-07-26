from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing_extensions import Annotated

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    """db will Session"""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_skip_limit(skip: int = 0, limit: int = 2):
    return skip, limit


PaginationParameters = Annotated[dict, Depends(get_skip_limit)]


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    pagination_parameters: PaginationParameters, db: Session = Depends(get_db)
):
    """response_model showing in docs like expected type, also validates input"""
    return crud.get_authors_list(
        db=db, skip=pagination_parameters[0], limit=pagination_parameters[1]
    )


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:

        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400, detail="Such name for Author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    pagination_parameters: PaginationParameters,
    db: Session = Depends(get_db),
    author_id: int | None = None,
):
    return crud.get_books_list(
        db=db,
        author_id=author_id,
        skip=pagination_parameters[0],
        limit=pagination_parameters[1],
    )


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    if crud.validate_author_id(db, book.author_id):
        raise HTTPException(
            status_code=404, detail=f"Author with id {book.author_id} not found"
        )
    return crud.create_book(db=db, book=book)
