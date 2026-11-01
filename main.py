from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

import crud
from database import Base, SessionLocal, engine
from schemas import AuthorCreate, AuthorSchema, BookCreate, BookSchema

# Створюємо таблиці за моделями (якщо їх ще немає)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/authors/", response_model=AuthorSchema, status_code=201)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    if crud.get_author_by_name(db, author.name):
        raise HTTPException(status_code=400, detail="Author with this name already exists")
    return crud.create_author(db, author)

@app.get("/authors/", response_model=list[AuthorSchema])
def read_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_authors(db, skip=skip, limit=limit)

@app.get("/authors/{author_id}", response_model=AuthorSchema)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@app.post("/authors/{author_id}/books/", response_model=BookSchema, status_code=201)
def create_book_for_author(
    author_id: int,
    book: BookCreate,
    db: Session = Depends(get_db),
):
    if crud.get_author(db, author_id) is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db, book, author_id)

@app.get("/books/", response_model=list[BookSchema])
def read_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    author_id: int | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
