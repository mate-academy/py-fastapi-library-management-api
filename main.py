from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import models
from database import SessionLocal, engine


def create_db_and_tables():
    models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to DB")
    create_db_and_tables()

    yield

    print("Closing DB")


app = FastAPI(lifespan=lifespan)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.AuthorsList])
def read_all_authors(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return crud.get_authors_list(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.AuthorsList)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.AuthorsList)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db=db, author_id=author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@app.post("/books/", response_model=schemas.BooksList)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db=db, author_id=book.author_id)

    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.BooksList])
def read_books(
    author_id: int | None= None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return crud.get_books_list(db=db, author_id=author_id, skip=skip, limit=limit)
