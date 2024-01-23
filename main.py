from fastapi import FastAPI, Depends, HTTPException, Query
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


@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exists!"
        )

    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=0),
    offset: int = Query(0, ge=0)
):
    return crud.get_all_authors(db=db, limit=limit, offset=offset)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/books/", response_model=schemas.BookCreate)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    db_book = crud.get_book_by_title(db=db, title=book.title)

    if db_book:
        raise HTTPException(
            status_code=400,
            detail="Book with this title already exists!"
        )

    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    author_id: int = None,
    db: Session = Depends(get_db),
):
    return crud.get_book_list(db=db, author_id=author_id)
