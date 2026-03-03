from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from crud import create_author, author_list, get_author_by_id, create_book, book_list
from database import SessionLocal
from fastapi import FastAPI, Depends, HTTPException

from models import Author
from schemas import AuthorBase, AuthorCreateSchema, BookCreateSchema, BookReadSchema

app = FastAPI()

def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/author", response_model=AuthorBase)
async def create_authors(authors_info: AuthorCreateSchema, db: Session = Depends(get_db)):
    db_author_request = db.execute(select(Author).where(Author.name == authors_info.name))
    result = db_author_request.scalar_one_or_none()

    if result is not None:
        raise HTTPException(status_code=400, detail="Author already exists")


    author = create_author(db=db, author_date=authors_info)

    return author


@app.get("/authors", response_model=List[AuthorBase])
async def get_authors(
        db: Session = Depends(get_db),
        skip: Optional[int] = None,
        limit: Optional[int] = None
):
    authors = author_list(db=db, skip=skip, limit=limit)

    if not authors:
        raise HTTPException(status_code=404, detail="No authors found")

    return authors


@app.get("/author/{author_id}", response_model=AuthorBase)
async def get_author( author_id: int, db: Session = Depends(get_db)):
    author = get_author_by_id(db=db, author_id=author_id)

    return author


@app.post("/books", response_model=BookReadSchema)
async def create_books(
        books_info: BookCreateSchema,
        db: Session = Depends(get_db)
):
    db_author = db.execute(select(Author).where(Author.id == books_info.author_id))
    author = db_author.scalar_one_or_none()

    if not author:
        raise HTTPException(status_code=400, detail="Author not found")

    book = create_book(book_date=books_info, db=db)

    return book


@app.get("/books", response_model=list[BookReadSchema])
async def get_books(
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        db: Session = Depends(get_db),
        author_id: Optional[int] = None
):
    if author_id:
        return book_list(db=db, skip=skip, limit=limit, author_id=author_id)


    books = book_list(db=db, skip=skip, limit=limit)

    return books