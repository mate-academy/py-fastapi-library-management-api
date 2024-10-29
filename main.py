from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(db: Session = Depends(get_db), limit: int = 10, skip: int = 0):
    return crud.get_all_authors(db=db, limit=limit, skip=skip)


@app.get("/authors/{pk}", response_model=schemas.Author)
def get_author(pk: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db=db, author_id=pk)


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, author_name=author.name)

    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def get_books(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
):
    return crud.get_all_books(db=db, skip=skip, limit=limit, author_id=author_id)


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    return crud.create_book(db=db, book=book)
