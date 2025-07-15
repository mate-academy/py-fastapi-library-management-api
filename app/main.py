from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.orm import Session

from app.crud import (
    get_all_authors,
    create_author,
    create_book,
    get_author_by_id,
    get_all_books,
    check_author_by_name_in_db
)
from app.db.database import get_db
from app.schemas import (
    AuthorListSchema,
    AuthorCreateSchema,
    BookListSchema,
    BookCreateSchema,
    AuthorRetrieveSchema
)

app = FastAPI()


@app.post("/authors/", response_model=AuthorListSchema)
def add_author(author: AuthorCreateSchema, db: Session = Depends(get_db)):
    if check_author_by_name_in_db(db=db, author_name=author.name):
        raise HTTPException(status_code=400, detail="Author already exists")
    return create_author(db, author)


@app.get("/authors/", response_model=List[AuthorListSchema])
def list_authors(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100)
):
    authors = get_all_authors(db=db, skip=skip, limit=limit)
    if not authors:
        raise HTTPException(status_code=404, detail="Authors not found")
    return authors


@app.get("/authors/{author_id}", response_model=AuthorRetrieveSchema)
def retrieve_author(author_id: int, db: Session = Depends(get_db)):
    author = get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/books/", response_model=BookListSchema)
def add_book(book: BookCreateSchema, db: Session = Depends(get_db)):
    return create_book(db, book)


@app.get("/books/", response_model=List[BookListSchema])
def list_books(
        db: Session = Depends(get_db),
        author_id: int = Query(None),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100)
):
    books = get_all_books(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit
    )
    if not books:
        raise HTTPException(status_code=404, detail="Books not found")
    return books
