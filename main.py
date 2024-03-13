from typing import Union

from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi_pagination import add_pagination, Page, paginate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

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


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/authors/")
def read_authors(db: Session = Depends(get_db)) -> Page[schemas.AuthorList]:
    return paginate(crud.get_all_authors(db))


@app.get("/authors/{author_id}/", response_model=schemas.AuthorRetrive)
def retrive_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.AuthorList)
def create_author(author_create: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author_create=author_create)


@app.get("/books/")
def get_all_books(db: Session = Depends(get_db), author: int | None = None) -> Page[schemas.BookList]:
    return paginate(crud.get_all_books(db=db, author=author))


@app.get("/books/{book_id}/", response_model=schemas.BookRetrive)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db=db, book_id=book_id)

    if db_book:
        db_author = crud.get_author_by_id(db=db, author_id=db_book.author_id)
        db_book.author = db_author
        return db_book

    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books/", response_model=schemas.BookCreate)
def create_book(book_create: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book_create=book_create)


add_pagination(app)
