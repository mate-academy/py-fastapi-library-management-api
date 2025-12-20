from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

import crud
from database import SessionLocal, Base, engine
from schemas import (
    AuthorListSchema,
    AuthorDetailSchema,
    AuthorResponseSchema,
    BookResponseSchema,
    BookCreateSchema,
    AuthorCreateSchema)


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.post("/authors/", response_model=AuthorResponseSchema)
def add_author(author: AuthorCreateSchema, db: Session = Depends(get_db)):
    return crud.create_new_author(db, author)


@app.post("/books/{author_id}/", response_model=BookResponseSchema)
def add_book(author_id: int, book: BookCreateSchema, db: Session = Depends(get_db)):
    return crud.add_book_by_author_id(db, author_id, book)


@app.get("/authors/", response_model=list[AuthorListSchema])
def get_authors_list(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return crud.get_all_authors_with_pagination(db, skip, limit)


@app.get("/authors/{author_id}/", response_model=AuthorDetailSchema)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db, author_id)


@app.get("/books/", response_model=list[BookResponseSchema])
def get_all_books(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(0, ge=10),
        author_id: int | None = Query(
            None,
        description="Filter books by author id"),
):
    return crud.get_all_books_with_pagination(db, skip, limit, author_id)
