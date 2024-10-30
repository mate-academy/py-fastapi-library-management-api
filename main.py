from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello world!"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 1
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=400,
            detail="Author with current id none exist"
        )

    return db_author


@app.post("authors", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
):

    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with current name already exist"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_book(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 1,
        author_id: int | None = None
):
    return crud.get_all_books(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id
    )


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_single_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(
            status_code=400,
            detail="Book with current id none exist"
        )

    return db_book


@app.post("/books/", response_model=schemas.Book)
def create_book( book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.book_create(db=db, book=book)
