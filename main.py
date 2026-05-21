from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

from database import SessionLocal, engine
import models
import schemas
import crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors", response_model=schemas.AuthorResponse)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(author, db)


@app.get("/authors", response_model=list[schemas.AuthorResponse])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorResponse)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(author_id, db)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.delete("/authors/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    return crud.delete_author(author_id, db)


@app.post("/authors/{author_id}/books", response_model=schemas.BookResponse)
def create_book(
    book: schemas.BookCreate, author_id: int, db: Session = Depends(get_db)
):
    return crud.create_book(author_id, book, db)


@app.get("/books", response_model=list[schemas.BookResponse])
def read_books(
    db: Session = Depends(get_db),
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
):
    if author_id is not None:
        return crud.get_books_by_author(author_id, db, skip=skip, limit=limit)
    return crud.get_all_books(db, skip=skip, limit=limit)


@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(book_id, db)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return crud.delete_book(book_id, db)
