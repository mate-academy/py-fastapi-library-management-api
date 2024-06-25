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


@app.post("/author/create/", response_model=schemas.AuthorList)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.AuthorList])
def get_all_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/author/{author_id}/", response_model=schemas.AuthorList)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db=db, author_id=author_id)


@app.post("/book/create/", response_model=schemas.BookCreate)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.BookList])
def get_all_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_books(skip=skip, limit=limit, db=db)


@app.get("/book/{id}/", response_model=schemas.BookList)
def get_book_by_author_it(author_id: int, db: Session = Depends(get_db)):
    return crud.get_book_by_author_id(author_id=author_id, db=db)
