from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal
from schemas import Author

app = FastAPI()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Hello world"}

@app.get("/authors/", response_model=list[schemas.Author])
def author_read(db: Session = Depends(get_db), page: int = 0, limit: int = 10):
    author = crud.get_all_authors(db, page=page, limit=limit)
    return author

@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db, author_name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exist")

    db_author = crud.author_create(db=db, author=author)
    return db_author

@app.get("/books/", response_model=list[schemas.Book])
def book_read(
            db: Session = Depends(get_db),
        author_id: int = None,
        page: int = 0,
        limit: int = 10
):
    book = crud.get_all_books(db, author_id=author_id, page=page, limit=limit)
    return book


@app.post("/books/create/", response_model=schemas.Book)
def book_create(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
