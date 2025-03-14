from typing import List

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

from app.crud import (
    create_author,
    get_author,
    get_list_authors,
    create_book,
    get_list_books
)
from app.database import SessionLocal, Base, engine
from app.schemas import (
    CreateAuthorSchema,
    AuthorGetSchema,
    BookGetSchema,
    CreateBookSchema
)

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=List[AuthorGetSchema])
def get_list_authors_endpoint(
        db: Session = Depends(get_db),
        offset: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=20),
):
    return get_list_authors(db=db, offset=offset, limit=limit)


@app.get("/author/{author_id}", response_model=AuthorGetSchema)
def get_author_endpoint(author_id: int, db: Session = Depends(get_db)):
    return get_author(db, author_id)


@app.post("/author-create/")
def create_author_endpoint(
        author_data: CreateAuthorSchema,
        db: Session = Depends(get_db)
):
    return create_author(db, author_data)


@app.get("/books/", response_model=List[BookGetSchema])
def get_list_books_endpoint(
        author_id: int,
        db: Session = Depends(get_db),
        offset: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=20),
):
    return get_list_books(
        db=db,
        offset=offset,
        limit=limit,
        author_id=author_id
    )


@app.post("/book-create/", response_model=BookGetSchema)
def create_book_endpoint(
        book_data: CreateBookSchema,
        db: Session = Depends(get_db)
):
    return create_book(db, book_data)
