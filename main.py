from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine

import schemas
import crud
from crud import get_author_by_name
from database import SessionLocal

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10,
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.CreateAuthor,
        db: Session = Depends(get_db)
):
    db_author = get_author_by_name(db=db, author_name=author.name)

    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None,
):
    return crud.get_all_books(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id
    )


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.CreateBook,
        db: Session = Depends(get_db),
):
    db_book = crud.get_book_by_title(db=db, book_title=book.title)

    if db_book:
        raise HTTPException(status_code=400, detail="Book already exists")

    return crud.create_book(db=db, book=book)
