from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
from db.engine import SessionLocal
from crud import create_authors, list_of_authors, get_author, create_book, list_of_books

app = FastAPI()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "hello"}


@app.post("/create_author/", response_model=schemas.Author)
def create_author(author_create: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return create_authors(db, author_create)


@app.get("/authors/", response_model=list[schemas.Author])
def list_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return list_of_authors(db, skip, limit)


@app.get("/author/{author_id}/", response_model=schemas.Author)
def get_author_by_id(author_id, db: Session = Depends(get_db)):
    result = get_author(db, author_id)
    if result:
        return result
    return HTTPException(
        status_code=404,
        detail="User unknown"
    )


@app.post("/create_book/", response_model=schemas.Book)
def create_book_for_author(book_create: schemas.BookCreate, db: Session = Depends(get_db)):
    return create_book(db, book_create)


@app.get("/books/", response_model=list[schemas.Book])
def list_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), author_id: int | None = None):
    return list_of_books(skip, limit, db, author_id)