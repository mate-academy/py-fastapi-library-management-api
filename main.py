from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db, engine
from models import Base

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/books/", response_model=List[schemas.Book])
def read_books(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
        author: int | None = None
) -> List[type[schemas.Book]]:
    return crud.get_all_books(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author
    )

@app.get("/books/{pk}/", response_model=schemas.Book)
def read_book(pk: int, db: Session = Depends(get_db)) -> type[schemas.Book]:
    book = crud.get_book(db=db, book_id=pk)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book

@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.Book:
    db_author = crud.get_author_by_id(db=db, author_id=book.author_id)
    if not db_author:
        raise HTTPException(status_code=400, detail="Author not found")

    return crud.create_book(
        db=db,
        book=book,
    )

@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> List[type[schemas.Author]]:

    return crud.get_all_authors(db=db, skip=skip, limit=limit)

@app.get("/authors/{pk}/", response_model=schemas.Author)
def read_author(
        pk: int,
        db: Session = Depends(get_db)
) -> type[schemas.Author]:
    author = crud.get_author_by_id(db=db, author_id=pk)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author

@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author_by_name(db=db, author_name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="This author already exists"
        )

    return crud.create_author(
        db=db,
        author=author,
    )
