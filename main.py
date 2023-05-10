from fastapi import FastAPI, Depends, HTTPException
from fastapi_pagination import add_pagination, Page, paginate
from sqlalchemy.orm import Session
from http import HTTPStatus

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


@app.get("/authors/", response_model=Page[schemas.Author])
def get_author_list(
        author_id: int = None,
        author_name: str = None,
        limit: int = None,
        db: Session = Depends(get_db)
) -> Page[schemas.Author]:
    authors = paginate(
        crud.get_author_list(
            db=db,
            author_id=author_id,
            author_name=author_name,
            limit=limit,
        ),
    )

    return authors


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_author_by_id(
        author_id: int = None,
        db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Author not found"
        )

    return db_author


@app.post("/authors/", response_model=schemas.AuthorBase)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> schemas.AuthorBase:
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Author with this name already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=Page[schemas.Book])
def get_book_list(
        author_id: int = None,
        author_name: str = None,
        book_title: str = None,
        limit: int = None,
        db: Session = Depends(get_db)
) -> Page[schemas.Book]:
    books = paginate(crud.get_book_list(
        db=db,
        author_id=author_id,
        author_name=author_name,
        book_title=book_title,
        limit=limit
        )
    )
    return books


@app.post("/books/", response_model=schemas.BookBase)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.BookBase:
    db_book = crud.get_book_by_title(db=db, book_title=book.title)

    if db_book is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Book with such title already exists"
        )
    return crud.create_book(db=db, book=book)


add_pagination(app)
