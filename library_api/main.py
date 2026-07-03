from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional


import database, models, schemas, crud

# Create database tables automatically
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Library Management API")


# Dependency to get db session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Author Endpoints ---

@app.post("/authors/", response_model=schemas.AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author name already registered")
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.AuthorResponse])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.AuthorResponse)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


# --- Book Endpoints ---

@app.post("/authors/{author_id}/books/", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def create_book_for_author(author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=List[schemas.BookResponse])
def read_books(
    skip: int = 0, 
    limit: int = 100, 
    author_id: Optional[int] = None, 
    db: Session = Depends(get_db)
):
    books = crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
    return books
