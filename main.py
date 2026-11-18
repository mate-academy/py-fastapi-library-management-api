from typing import List, Annotated

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
def read_root():
    return {"Hello": "World"}


@app.get("/authors/", response_model=List[schemas.Author])
def read_author_list(
        db: Session = Depends(get_db),
        offset: int = 0,
        limit: Annotated[int, Query(le=3)] = 3,
):
    return crud.get_authors(db=db, offset=offset, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author_id(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_id(db=db, author_id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="this author already exists")
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=List[schemas.Book])
def read_book_list(
        db: Session = Depends(get_db),
        offset: int = 0,
        limit: Annotated[int, Query(le=3)] = 3,
        author_id: Annotated[int | None, Query(ge=1)] = None,
):
    return crud.get_books(db=db, offset=offset, limit=limit, author_id=author_id)


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    db_book = crud.get_book_title(db=db, title=book.title)

    if db_book:
        raise HTTPException(status_code=400, detail="this book already exists")
    return crud.create_book(db=db, book=book)

@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book_id(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_id(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book