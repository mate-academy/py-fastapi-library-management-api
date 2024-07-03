from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import (
    get_all_authors,
    get_author_by_name,
    create_author_crud,
    get_all_books,
    create_book_crud,
    get_author_by_id_crud)
from database import SessionLocal
from models import DBAuthors
from schemas import AuthorsList, AuthorsCreate, BookList, BookCreate

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[AuthorsList])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 5
) -> list:
    authors = get_all_authors(db=db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=AuthorsList)
def get_author_by_id(
        author_id: int,
        db: Session = Depends(get_db)
) -> Optional[DBAuthors]:
    db_author = get_author_by_id_crud(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )
    return db_author


@app.post("/authors/", response_model=AuthorsList)
def create_author(
        author: AuthorsCreate,
        db: Session = Depends(get_db)
) -> DBAuthors:
    db_author = get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400, detail="Such name fo Author already exists"
        )
    return create_author_crud(db=db, author=author)


@app.get("/books/", response_model=list[BookList])
def read_books(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 3,
        author_id: Optional[int] = None
) -> list:
    return get_all_books(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id
    )


@app.post("/books/", response_model=BookList)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return create_book_crud(db=db, book=book)
