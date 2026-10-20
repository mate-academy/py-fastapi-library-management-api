from fastapi import FastAPI, Depends, HTTPException

from database import SessionLocal
import models

import crud
import schemas

app = FastAPI()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_author_by_name(db: SessionLocal, name: str):
    return db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()

def get_book_by_title(db: SessionLocal, title: str):
    return db.query(models.DBBook).filter(models.DBBook.title == title).first()


@app.get('/')
def root():
    return { 'message': 'Hello World!' }


@app.get('/authors/', response_model=list[schemas.AuthorRead])
def get_authors(db: SessionLocal = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_authors(db, skip, limit)


@app.post('/authors/', response_model=schemas.AuthorRead)
def create_author(author: schemas.AuthorCreate, db: SessionLocal = Depends(get_db)):
    if get_author_by_name(db, author.name):
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(db, author)

@app.get('/authors/{author_id}', response_model=schemas.AuthorRead)
def get_author_detail(author_id: int, db: SessionLocal = Depends(get_db)):
    return crud.get_author_detail(db, author_id)


@app.post('/books/', response_model=schemas.BookRead)
def create_book(book: schemas.BookCreate, db: SessionLocal = Depends(get_db)):
    if get_book_by_title(db, book.title):
        raise HTTPException(status_code=400, detail="Book already exists")
    return crud.create_book(db, book)


@app.get('/books/', response_model=list[schemas.BookRead])
def get_books(db: SessionLocal = Depends(get_db), skip: int = 0, limit: int = 100, author_id: int = None):
    return crud.get_books(db, skip, limit, author_id)