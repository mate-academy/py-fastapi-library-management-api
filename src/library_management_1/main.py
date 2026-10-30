from collections.abc import Iterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import Base, SessionLocal, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Library Management API", version="1.0.0", lifespan=lifespan)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbDep = Annotated[Session, Depends(get_db)]
SkipQ = Annotated[int, Query(ge=0)]
LimitQ = Annotated[int, Query(ge=1, le=100)]


# ---- Authors ----
@app.post("/authors/", response_model=schemas.Author, status_code=201)
def create_author(author: schemas.AuthorCreate, db: DbDep):
    if crud.get_author_by_name(db, author.name):
        raise HTTPException(status_code=409, detail="Author with this name already exists")
    return crud.create_author(db, author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(db: DbDep, skip: SkipQ = 0, limit: LimitQ = 100):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: DbDep):
    author = crud.get_author(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book, status_code=201)
def create_book_for_author(author_id: int, book: schemas.BookCreate, db: DbDep):
    if crud.get_author(db, author_id) is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_author_book(db, book, author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    db: DbDep,
    skip: SkipQ = 0,
    limit: LimitQ = 100,
    author_id: int | None = None,
):
    """List books with pagination. Pass `author_id` to filter by author."""
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
