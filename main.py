from fastapi import FastAPI, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage, add_pagination, paginate
from sqlalchemy.orm import Session

import database
import schemas
import crud


app = FastAPI()
add_pagination(app)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=LimitOffsetPage[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    return paginate(crud.get_authors(db))


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db, author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists.")

    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_id(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=400, detail="Author does not exist.")

    return db_author


@app.post("/authors/{author_id}/", response_model=schemas.Book)
def create_book_for_specific_author(
        author_id: int,
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book_for_author(db=db, author_id=author_id, book=book)


@app.get("/books/", response_model=LimitOffsetPage[schemas.Book])
def read_books(
        author_id: int | None = None,
        db: Session = Depends(get_db)
):
    return paginate(crud.get_books_list(db=db, author_id=author_id))
