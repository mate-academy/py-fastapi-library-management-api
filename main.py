from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def list_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_authors(skip=skip, limit=limit, db=db)


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400, detail="This author is already exist in DB"
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def retrieve_author_by_id(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author:
        return db_author
    raise HTTPException(
        status_code=404, detail="Author not found"
    )


@app.get("/books/", response_model=list[schemas.Book])
def list_books(author_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_books(skip=skip, limit=limit, db=db, author_id=author_id)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_title(db=db, title=book.title)
    if db_book:
        raise HTTPException(
            status_code=400, detail="This book is already exist in DB"
        )
    return crud.create_book(db=db, book=book)
