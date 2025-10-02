from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from library.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/author", response_model=list[schemas.Author])
def get_all_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db)


@app.post("/author", response_model=schemas.Author)
def create_new_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    existing_author = crud.get_author(db, author.name)
    if existing_author:
        raise HTTPException(status_code=400, detail="Author type already exists")
    return crud.create_new_author(db, author)


@app.get("/author/{author_id}/", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.get("/book", response_model=list[schemas.Book])
def read_books(db: Session = Depends(get_db)):
    return crud.get_book_list(db)


@app.post("/book", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    existing_book = crud.get_book(db, book.title)
    if existing_book:
        raise HTTPException(status_code=400, detail="Book type already exists")
    return crud.create_book(db, book)


@app.get("/book/{book_id}/", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book
