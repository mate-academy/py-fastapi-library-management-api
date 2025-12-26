from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db import models
from database import SessionLocal, engine
import crud
from schemas import AuthorRead, AuthorCreate, BookCreate, BookRead

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "fastapi-library-management-api"}


@app.post("/authors/", response_model=AuthorRead)
def create_author(
    author: AuthorCreate,
    db: Session = Depends(get_db)
):
    return crud.create_author(db, author)


@app.get("/authors/", response_model=list[AuthorRead])
def get_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    return crud.get_authors(db, skip, limit)


@app.get("/authors/{author_id}", response_model=AuthorRead)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/{author_id}/books/", response_model=BookRead)
def create_book_for_author(
    author_id: int,
    book: BookCreate,
    db: Session = Depends(get_db)
):
    author = crud.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_book(db, author_id, book)


@app.get("/books/", response_model=list[BookRead])
def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    return crud.get_books(db, skip, limit)


@app.get("/authors/{author_id}/books/", response_model=list[BookRead])
def get_books_by_author(
    author_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    author = crud.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.get_books_by_author(db, author_id, skip, limit)


