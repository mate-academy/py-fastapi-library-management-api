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


@app.get("/authors", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_author_list(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(status_code=404, detail="Such Author already exist")

    return crud.create_author(db=db, author=author)


@app.get("/books", response_model=list[schemas.Book])
def read_books(
    author_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_book_list(db=db, skip=skip, limit=limit, author_id=author_id)


@app.post("/books", response_model=schemas.Book)
def create_book(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book, author_id=author_id)
