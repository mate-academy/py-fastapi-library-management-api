from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

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
async def root():
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors_list(db: Session = Depends(get_db),
                     skip: int = 0,
                     limit: int = 5):
    return crud.get_all_authors(db, skip, limit)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=409,
            detail="Author already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_author_details(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db=db, author_id=author_id)
    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )
    return author


@app.get("/books/", response_model=list[schemas.Book])
def get_all_books(db: Session = Depends(get_db),
                  skip: int = 0,
                  limit: int = 5):
    return crud.get_all_books(db, skip, limit)


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
):
    db_book = crud.get_book_by_title(db=db, title=book.title)
    if db_book:
        raise HTTPException(
            status_code=400,
            detail="Book already exists"
        )
    return crud.create_book(db=db, book=book)


@app.get("/books/{author_id}/", response_model=list[schemas.Book])
def get_book_details(author_id: int, db: Session = Depends(get_db)):
    books = crud.get_authors_books(db=db, author_id=author_id)
    if not books:
        raise HTTPException(
            status_code=404,
            detail="Books for the given author were not found"
        )
    return books
