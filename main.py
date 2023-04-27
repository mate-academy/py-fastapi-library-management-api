from fastapi import FastAPI, HTTPException, Depends
from fastapi.params import Query
from sqlalchemy.orm import Session
from typing import List
import models, schemas, crud, database

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


# Dependency function for database sessions
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API endpoints
@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def get_authors(skip: int = Query(0), limit: int = Query(10), db: Session = Depends(get_db)):
    authors = crud.get_all_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=List[schemas.Book])
def get_books(skip: int = Query(0), limit: int = Query(10), db: Session = Depends(get_db)):
    books = crud.get_all_books(db, skip=skip, limit=limit)
    return books


@app.get("/books/author/{author_id}", response_model=List[schemas.Book])
def get_books_by_author(author_id: int, db: Session = Depends(get_db)):
    books = crud.get_books_by_author(db, author_id=author_id)
    return books
