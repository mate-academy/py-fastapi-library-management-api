from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import crud
from database import SessionLocal, engine
from models import Base
from schemas import AuthorCreateSchema, AuthorSchema, BookCreateSchema, BookSchema

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


# dependency для БД-сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors", response_model=AuthorSchema, status_code=201)
def create_author(author: AuthorCreateSchema, db: Session = Depends(get_db)):
    try:
        return crud.create_author(db, author)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Author with this name already exists")


@app.get("/authors", response_model=list[AuthorSchema])
def list_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=AuthorSchema)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/{author_id}/books", response_model=BookSchema, status_code=201)
def create_book_for_author(
    author_id: int,
    book: BookCreateSchema,
    db: Session = Depends(get_db),
):
    author = crud.get_author_by_id(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book_for_author(db, author_id=author_id, book_in=book)


@app.get("/books", response_model=list[BookSchema])
def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    author_id: int | None = Query(None, ge=1),
    db: Session = Depends(get_db),
):
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
