from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.AuthorRead, status_code=201)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    existing = crud.get_author_by_name(db, name=author.name)
    if existing:
        raise HTTPException(status_code=400, detail="Author with this name already exists")
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.AuthorRead])
def read_authors(
    skip: int = Query(0, ge=0), limit: int = Query(100, ge=1), db: Session = Depends(get_db)
):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/{author_id}/books/", response_model=schemas.BookRead, status_code=201)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.BookRead])
def read_books(
    author_id: int | None = Query(None, alias="authorId"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    db: Session = Depends(get_db),
):
    if author_id is not None:
        return crud.get_books_by_author(db, author_id=author_id, skip=skip, limit=limit)
    return crud.get_books(db, skip=skip, limit=limit)
