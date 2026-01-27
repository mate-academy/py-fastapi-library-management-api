from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import models, schemas, crud
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Library Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    existing_author = crud.get_author_by_name(db, author.name)
    if existing_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db, author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)



@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
    db: Session = Depends(get_db)
):
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)



@app.get("/books/", response_model=List[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 10,
    author_id: Optional[int] = Query(None, description="Filter books by author ID"),
    db: Session = Depends(get_db)
):
    books = crud.get_books(db)
    if author_id is not None:
        books = [book for book in books if book.author_id == author_id]
    return books[skip: skip + limit]
