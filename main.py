from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API",
    description="Test API",
    version="1.0.0",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author, status_code=201, tags=["Authors"])
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    if crud.get_author_by_name(db, name=author.name):
        raise HTTPException(status_code=400, detail="Author with this name already exists.")
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.AuthorSummary], tags=["Authors"])
def list_authors(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max records to return"),
    db: Session = Depends(get_db),
):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author, tags=["Authors"])
def get_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found.")
    return db_author


@app.post(
    "/authors/{author_id}/books/",
    response_model=schemas.Book,
    status_code=201,
    tags=["Books"],
)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    if crud.get_author(db=db, author_id=author_id) is None:
        raise HTTPException(status_code=404, detail="Author not found.")
    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=List[schemas.Book], tags=["Books"])
def list_books(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max records to return"),
    author_id: Optional[int] = Query(None, description="Filter books by author ID"),
    db: Session = Depends(get_db),
):
    return crud.get_books(db=db, skip=skip, limit=limit, author_id=author_id)
