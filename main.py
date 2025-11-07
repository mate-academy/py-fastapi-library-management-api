from typing import Any
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

import crud
import schemas
from database import engine, LocalSession, Base
from models import DBAuthor, DBBook


Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db() -> Session:
    db = LocalSession()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {
        "message": "Hello, here you can work with Author and Book data bases."
    }

@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
) -> Any:
    existing_author = (
        db.query(DBAuthor)
        .filter(DBAuthor.name == author.name)
        .first()
    )
    if existing_author:
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exists."
        )

    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> Any:
    authors = crud.get_author_list(db, skip=skip, limit=limit)
    return authors


@app.get("/author/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)) -> Any:
    author = crud.get_author(db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/book/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)) -> Any:
    author = crud.get_author(db, author_id=book.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def get_books(
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
    db: Session = Depends(get_db)
) -> Any:
    books = crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
    return books
