
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import schemas, crud
from database import Base, engine, SessionLocal
from models import Book, Author


app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@app.get("/author/",
         response_model=list[schemas.AuthorRead])
def read_author(skip: int = 0,
                limit: int = 10,
                db=Depends(get_db)):
    return crud.get_all_authors(db, skip, limit)


@app.get("/author/{author_id}", response_model=schemas.AuthorRead)
def read_single_author(author_id: int,
                       db=Depends(get_db)):
    author = crud.get_single_author(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/author/",
          response_model=schemas.AuthorRead,
          status_code=201)
def create_author(author: schemas.AuthorCreate,
                  db=Depends(get_db)):
    try:
        return crud.create_author(db, author)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Author name already exists")


@app.get("/book/", response_model=list[schemas.BookRead])
def read_book(skip: int = 0,
              limit: int = 10,
              author_id: int | None = None,
              db=Depends(get_db),
              ):
    if author_id is not None:
        return crud.filter_book(db, author_id, skip, limit)
    return crud.get_all_books(db, skip, limit)


@app.post("/book/",
          response_model=schemas.BookRead,
          status_code=201)
def create_book(book: schemas.BookCreate, db=Depends(get_db)):
    if crud.get_single_author(db, book.author_id) is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db, book)
