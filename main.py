from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

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


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[schemas.AuthorList])
def read_all_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorList)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return db_author


@app.post("/authors/", response_model=schemas.AuthorList)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    author_name = crud.get_author_by_name(db=db, name=author.name)
    if author_name:
        raise HTTPException(
            status_code=400,
            detail="There is already author with such name in the system"
        )
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.BookList])
def read_all_books(
        author_id: int,
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10,
):
    db_book = crud.get_all_books(db, author_id=author_id, skip=skip, limit=limit)

    if db_book is None:
        return HTTPException(
            status_code=404,
            detail="Book not found"
        )
    return db_book


@app.post("/books/", response_model=schemas.BookCreate)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    book_title = crud.get_book_by_title(db=db, title=book.title)
    if book_title:
        raise HTTPException(
            status_code=400,
            detail="There is already book with such title in the system"
        )
    return crud.create_book(db=db, book=book)
