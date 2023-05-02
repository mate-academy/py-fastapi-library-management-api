from fastapi import FastAPI, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.orm import Session

import crud
import schemas
from db import models
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"Hello": "World"}


@app.get("/authors", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> schemas.Author:
    return crud.create_author(db=db, author=author)


@app.get("/books", response_model=list[schemas.Book])
def read_books(author_id: int = Query(None), db: Session = Depends(get_db)):
    if author_id:
        db_author = crud.get_author(db, author_id=author_id)
        if db_author is None:
            raise HTTPException(status_code=404, detail="Author not found")
        books = crud.get_books_by_author(db, author_id=author_id)
    else:
        books = crud.get_all_books(db)
    return books


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
