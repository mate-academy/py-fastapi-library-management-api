from typing import Optional

from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import crud
import schemas
from db import models
from db.database import SessionLocal
from lib_app.schemas import AuthorCreate

app = FastAPI()


def get_db() -> Session:
    db: SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/")
def read_authors(skip: int = 0,
                 limit: int = 10,
                 db: Session = Depends(get_db)) \
        -> Optional[models.Author]:
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorRetrive)
def retrieve_author(author_id: int, db: Session = Depends(get_db))\
        -> Optional[models.Author]:
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.AuthorList)
def create_author(author_create: schemas.AuthorCreate,
                  db: Session = Depends(get_db))\
        -> AuthorCreate:
    return crud.create_author(db=db, author=author_create)


@app.get("/books/")
def get_all_books(db: Session = Depends(get_db),
                  author: int | None = None,
                  skip: int = 0,
                  limit: int = 10) \
        -> Optional[models.Book]:
    return crud.get_all_books(db=db, author=author, skip=skip, limit=limit)


@app.get("/books/{book_id}/", response_model=schemas.BookRetrive)
def get_book(book_id: int, db: Session = Depends(get_db))\
        -> Optional[models.Book]:
    db_book = crud.get_book_by_id(db=db, book_id=book_id)

    if db_book:
        db_author = crud.get_author_by_id(db=db, author_id=db_book.author_id)
        db_book.author = db_author
        return db_book

    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books/", response_model=schemas.BookCreate)
def create_book(book_create: schemas.BookCreate,
                db: Session = Depends(get_db))\
        -> Optional[models.Book]:
    return crud.create_book(db=db, book=book_create)


@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=500,
        content={
            "message": (
                f"Failed method {request.method} at URL {request.url}."
                f" Exception message is {exc!r}."
            )
        },
    )
