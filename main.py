from fastapi import FastAPI, Depends, HTTPException
from fastapi_pagination import Page, paginate, add_pagination
from sqlalchemy.orm import Session

import crud
import schemas
import uvicorn

from db import models
from db.engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "This is Fastapi Library manager API"}


@app.get("/authors/", response_model=Page[schemas.Author])
def read_authors(db: Session = Depends(get_db)) -> list[models.DBAuthor]:
    return paginate(crud.get_all_authors(db=db))


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(db: Session = Depends(get_db), author_id: int = 0) -> models.DBAuthor:
    return crud.get_author_by_id(db=db, author_id=author_id)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
) -> models.DBAuthor:
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400, detail="Such name for Author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=Page[schemas.Book])
def read_books(db: Session = Depends(get_db)) -> list[models.DBBook]:
    return paginate(crud.get_book_list(db=db))


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate, db: Session = Depends(get_db)
) -> models.DBBook:
    return crud.create_book(db=db, book=book)


@app.get("/book/{book_id}/", response_model=schemas.Book)
def read_single_book(book_id: int, db: Session = Depends(get_db)) -> models.DBBook:
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.get("/books/author/", response_model=list[schemas.Book])
def search_books_by_author(
    author_id: int, db: SessionLocal = Depends(get_db)
) -> models.DBBook:
    return crud.filter_books_by_author(db, author_id=author_id)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)


add_pagination(app)
