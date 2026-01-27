from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal

import schemas
import crud


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/author/", response_model=schemas.AuthorRead)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
):
    return crud.create_author(db, author)

@app.get("/authors/", response_model=list[schemas.AuthorRead])
def get_author(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
):
    return crud.get_authors(db, skip=skip, limit=limit)

@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@app.post(
    "/author/{author_id}/books/",
    response_model=schemas.BookRead,
)
def create_book_for_author(
        author_id: int,
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
):
    author = crud.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db, book, author_id)

@app.get("/books/", response_model=list[schemas.BookRead])
def get_books(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
):
    return crud.get_books(db, skip=skip, limit=limit)

@app.get(
    "/author/{author_id}/books/",
    response_model=list[schemas.BookRead],
)
def get_books_by_author(
        author_id: int,
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return crud.get_books_by_author(
        db,
        author_id=author_id,
        skip=skip,
        limit=limit
    )
