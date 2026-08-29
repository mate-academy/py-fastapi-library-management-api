from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/")
def create_author_endpoint(
    author: schemas.AuthorBase,
    db: Session = Depends(get_db),
):
    return crud.create_author(db, author)


@app.get("/authors/")
def read_authors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}")
def read_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author(db, author_id=author_id)


@app.post("/authors/{author_id}/books/")
def create_book_for_author(
    author_id: int,
    book: schemas.BookBase,
    db: Session = Depends(get_db),
):
    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/")
def read_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_books(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/books/")
def read_books_by_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_books_by_author(db, author_id=author_id)
