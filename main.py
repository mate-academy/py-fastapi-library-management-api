from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

DEFAULT_LIMIT = 3
DEFAULT_OFFSET = 0


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"description": "Library Management API", "version": "1.0"}


@app.get("/author/", response_model=list[schemas.Author])
def read_authors(
        limit: int = Query(DEFAULT_LIMIT, ge=0),
        offset: int = Query(DEFAULT_OFFSET, ge=0),
        db: Session = Depends(get_db)) -> list[schemas.Author]:
    return crud.get_all_authors(db=db, limit=limit, offset=offset)


@app.get("/author/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)) -> schemas.Author:
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail=f"Author id= {author_id} not found")

    return db_author


@app.post("/author/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
) -> schemas.Author:
    db_author = crud.get_author_type_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(status_code=400, detail="Author name already exists")

    return crud.create_author(db=db, author=author)


@app.get("/book/", response_model=list[schemas.Book])
def read_books(
        author_id: int | None = None,
        limit: int = Query(DEFAULT_LIMIT, ge=0),
        offset: int = Query(DEFAULT_OFFSET, ge=0),
        db: Session = Depends(get_db),
) -> list[schemas.Book]:
    return crud.get_books_list(db=db, author_id=author_id, limit=limit, offset=offset)


@app.get("/book/{book_id}/", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)) -> schemas.Book:
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.post("/book/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)) -> schemas.Book:
    db_author = crud.get_author(db=db, author_id=book.author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail=f"Author id= {book.author_id} not found")

    return crud.create_book(db=db, book=book)
