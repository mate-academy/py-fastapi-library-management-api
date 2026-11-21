from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Library API is running"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_author_by_id(author_id: int, db=Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found.")
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    if crud.get_author_by_name(db=db, name=author.name) is not None:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db=db, author=author)


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found.")
    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None
):
    return crud.get_books(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id
    )
