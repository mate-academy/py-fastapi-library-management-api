from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session

from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination.ext.sqlalchemy import paginate as paginate_sql

import crud
import schemas
from db.engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/authors/", response_model=Page[schemas.AuthorRead])
def get_all_authors(db: Session = Depends(get_db)):
    return paginate(crud.get_all_authors(db=db))


@app.get("/authors/{author_id}/")
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(author_id=author_id, db=db)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@app.post("/autors/", response_model=schemas.AuthorRead)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=Page[schemas.BookRead])
def get_all_books(author_id: int = None, db: Session = Depends(get_db)):
    if author_id:
        return paginate_sql(crud.get_books_by_author_id(db=db, author_id=author_id))

    return paginate(crud.get_all_books(db=db))


@app.post("/books/", response_model=schemas.BookRead)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


add_pagination(app)
