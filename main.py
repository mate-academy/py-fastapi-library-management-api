from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "hello world!"}


@app.get("/authors/", response_model=list[schemas.AuthorList])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db)


@app.post("/authors/", response_model=schemas.AuthorList)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
):
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorList)
def get_single_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author(db, author_id)


@app.get("/books/", response_model=list[schemas.BookList])
def read_books(db: Session = Depends(get_db),
               author_id: int = None,
               skip: int = Query(0, alias="page"),
               limit: int = Query(0, alias="size")
               ):
    return crud.get_all_books(db=db, author_id=author_id, skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.BookList)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)
