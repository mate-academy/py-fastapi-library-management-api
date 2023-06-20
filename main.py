from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int, limit: int, db: Session = Depends(get_db)):
    db_authors = crud.get_authors(db, skip=skip, limit=limit)
    return db_authors


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    

@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.create_author(db=db, author=author)
    if db_author:
        raise HTTPException(status_code=400, detail="Author with defined name already exsist")
    return db_author


@app.get("/books/", response_model=schemas.Book)
def get_books(skip: int, limit: int, db: Session = Depends(get_db)):
    db_books = crud.get_books(db, skip=skip, limit=limit)
    return db_books


@app.get("/books/{book_id}/", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.post("/books/", response_model=schemas.BookCreate)
def create_book(book: schemas.BookCreate, author_id: int, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book, author_id=author_id)
