from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal, Base, engine

app = FastAPI(title="Library Management API")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=0),
        db: Session = Depends(get_db)
):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author, status_code=201)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.get("/books/", response_model=List[schemas.Book])
def read_books(
        author_id: Optional[int] = None,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=0),
        db: Session = Depends(get_db)
):
    if author_id is not None:
        return crud.get_books_by_author(db=db, author_id=author_id, skip=skip, limit=limit)
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/books/by_author/{author_id}", response_model=List[schemas.Book])
def read_books_by_author(
    author_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return crud.get_books_by_author(db=db, author_id=author_id, skip=skip, limit=limit)


@app.post("/authors/{author_id}/books/", response_model=schemas.Book, status_code=201)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    db_author = crud.get_author(db=db, author_id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, book=book, author_id=author_id)
