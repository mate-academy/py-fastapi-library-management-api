from typing import Generator, Annotated

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine
from models import Author

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    "/authors/",
    response_model=list[schemas.Author],
)
async def get_authors(
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
):
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author)
async def create_author(
    author: schemas.AuthorCreate, db: Annotated[Session, Depends(get_db)]
):
    db_author = db.scalar(select(Author).where(Author.name == author.name))
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(db, author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
async def get_author(author_id: int, db: Annotated[Session, Depends(get_db)]):
    author = crud.get_author_by_id(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="No author with such id is found")
    return author


@app.get("/books/", response_model=list[schemas.Book])
async def get_books(
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
):
    return crud.get_all_books(db, skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.Book)
async def create_book(
    book: schemas.BookCreate, db: Annotated[Session, Depends(get_db)]
):
    if crud.get_author_by_id(db, book.author_id) is None:
        raise HTTPException(
            status_code=400, detail="Author with such id does not exist"
        )
    return crud.create_book(db, book)


@app.get("/authors/{author_id}/books/", response_model=list[schemas.Book])
def get_books_by_author(author_id: int, db: Annotated[Session, Depends(get_db)]):
    if crud.get_author_by_id(db, author_id) is None:
        raise HTTPException(status_code=404, detail="No author with such id")

    books = crud.get_books_by_author_id(db, author_id)
    return books
