import datetime

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_pagination import Page, add_pagination, paginate, Params

import crud
import schemas
from db.engine import SessionLocal

app = FastAPI()
add_pagination(app)

def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


@app.get("/authors/", response_model=Page[schemas.Author])
def read_authors(
    db: Session = Depends(get_db),
    params: Params = Depends(),
) -> Page[schemas.Author]:
    params.size = 5
    return paginate(crud.get_all_authors(db), params)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author_by_name(db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail=f"Author with name {author.name} already exists.")

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=Page[schemas.Book])
def read_books(
    author: str | None = None,
    db: Session = Depends(get_db),
    params: Params = Depends(),
) -> Page[schemas.Book]:
    params.size = 5
    return paginate(crud.get_book_list(
        db=db,
        author=author
    ), params
    )


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_single_book(
    book_id: int,
    db: Session = Depends(get_db),
) -> schemas.Book:
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return schemas.Book.from_orm(db_book)


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
) -> schemas.Book:
    return schemas.Book.from_orm(crud.create_book(db=db, book=book))
