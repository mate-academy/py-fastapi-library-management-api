from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return "Hello World"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create_author", response_model=schemas.AuthorBase)
def create_author(data: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, data)

@app.get("/authors", response_model=list[schemas.AuthorRead])
def get_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = crud.get_authors(db)
    return authors[skip: skip + limit]

@app.get("/author/{author_id}", response_model=schemas.AuthorRead)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail=f"There is not author with id {author_id}")
    return author


@app.post("/author/{author_id}/create_book", response_model=schemas.BookBase)
def create_book(author_id: int, data: schemas.BookCreate, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db=db,author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="You can't create a book for this author, because this author doesn't exist!")
    return crud.create_book(db=db, data=data, author_id=author_id)


@app.get("/book/{book_id}", response_model=schemas.BookRead)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book_by_id(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found!")
    return book

@app.get("/books", response_model=list[schemas.BookRead])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_books(db=db)
    return books[skip: skip + limit]

@app.get("/author/{author_id}/books", response_model=list[schemas.BookRead])
def get_books_by_author(author_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_books(db=db)
    if author_id is not None:
        books = [b for b in books if b.author_id == author_id]
    return books[skip: skip + limit]