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


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db), skip=0, limit=3):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author is not found")
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db=db, author=author)


@app.patch("/authors/{author_id}/", response_model=schemas.Author)
def update_author(author_id: int, author: schemas.Author, db: Session = Depends(get_db)):
    db_author = crud.author_update(db=db, author_id=author_id, author=author)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author is not found")
    return db_author


@app.delete("/authors/{author_id}/", response_model=schemas.Author)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.author_delete(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author is not found")
    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(db: Session = Depends(get_db), skip=0, limit=3):
    return crud.get_all_books(db=db, skip=skip, limit=limit)


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_single_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book is not found")
    return db_book


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_title(db=db, title=book.title)
    if db_book:
        raise HTTPException(status_code=400, detail="Book already exists")
    return crud.create_book(db=db, book=book)


@app.delete("/books/{book_id}/", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.book_delete(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book is not found")
    return db_book
