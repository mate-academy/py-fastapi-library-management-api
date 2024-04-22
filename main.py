from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

import crud
import database
import schemas

app = FastAPI()


def get_db() -> Session:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Welcome to our library!"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_author(
        skip: int | None,
        limit: int | None,
        db: Session = Depends(get_db)
):
    return crud.get_all_author(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    if crud.get_author_by_name(name=author.name, db=db):
        raise HTTPException(
            status_code=400,
            detail="Author with name already exists in DB!"
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author_by_id(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db=db, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_book(
        author_id: int | None = None,
        skip: int | None = 0,
        limit: int | None = 10,
        db: Session = Depends(get_db)
):
    return crud.get_books(db=db, skip=skip, limit=limit, author_id=author_id)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
