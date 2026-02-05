from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal, Base, engine


Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Library Management API"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    existing = crud.get_author_by_name(db, name=author.name)
    if existing:
        raise HTTPException(status_code=400, detail="Author already registered")
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
        author_id: int,
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    author = crud.get_author_by_id(db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book_for_author(db=db, author_id=author_id, book=book)


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.post("/books/", response_model=schemas.Book)
def read_books(
        skip: int = 0,
        limit: int = 100,
        author_id: int | None = None,
        db: Session = Depends(get_db),
):
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
