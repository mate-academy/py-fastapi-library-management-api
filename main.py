from typing import Generator, List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.params import Query, Path
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()

def get_db() -> Generator[None, Session, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors", response_model=List[schemas.Author])
def get_all_authors(
        skip: int = Query(default=0),
        limit: int = Query(default=10),
        db: Session = Depends(get_db)
) -> List[schemas.Author]:
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author_by_id(
        author_id: int = Path(),
        db: Session = Depends(get_db)
) -> schemas.Author:
    author = crud.get_author_by_id(db=db, author_id=author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@app.post("/authors", response_model=schemas.Author)
def create_cheese_type(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> schemas.Author:
    existing_author = crud.get_author_by_name(db=db, name=author.name)

    if existing_author:
        raise HTTPException(status_code=409, detail="Author with this name already exist")

    return crud.create_author(db=db, author=author)


@app.get("/books", response_model=List[schemas.Book])
def get_all_books_by_author_id(
        author_id: int = Query(),
        db: Session = Depends(get_db)
) -> List[schemas.Book]:
    author = crud.get_author_by_id(db=db, author_id=author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.get_all_books_by_author_id(db=db, author_id=author_id)


@app.get("/books", response_model=List[schemas.Book])
def get_all_books(
        skip: int = Query(default=0),
        limit: int = Query(default=10),
        db: Session = Depends(get_db)
) -> List[schemas.Book]:
    return crud.get_all_books(db=db, skip=skip, limit=limit)


@app.post("/books", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.Book:
    author = crud.get_author_by_id(db=db, author_id=book.author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_book(db=db, book=book)
