from typing import Any, Annotated, Generator

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import joinedload, Session

import crud
import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate, db: Session = Depends(get_db)
) -> models.Author:
    """
    Create a new author.
    """
    db_author = crud.get_author_by_name(db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    name: str = Query(
        None,
        title="Name",
        description="Search authors by name.",
        max_length=30,
        example="Dumas",
    ),
    sort_by: str = Query(
        None,
        title="Sort By",
        description="Sort authors by field (name or id).",
        max_length=30,
        example="name",
    ),
    sort_order: str = Query(
        "asc",
        title="Sort Order",
        description="Sort order (ascending or descending) for results.",
        max_length=4,
        example="desc",
    ),
    skip: int = Query(
        0,
        title="Skip",
        description="Number of records to skip.",
        ge=0,
        example=3,
    ),
    limit: int = Query(
        5,
        title="Limit",
        description="Maximum number of records to return.",
        ge=1,
        le=1000,
        example=10,
    ),
    db: Session = Depends(get_db),
) -> list[models.Author]:
    """
    Retrieve a list of authors with pagination (skip, limit), search and sorting functionality.
    """
    authors = crud.get_authors(
        db=db, name=name, sort_by=sort_by, sort_order=sort_order, skip=skip, limit=limit
    )
    return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)) -> Any:
    """
    Retrieve a single author by ID.
    """
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
) -> models.Book:
    """
    Create a new book for a specific author.
    """
    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    title: str = Query(
        None,
        title="Title",
        description="Search books by title.",
        max_length=60,
        example="Kobzar",
    ),
    sort_by: str = Query(
        None,
        title="Sort By",
        description="Sort books by field(title, publication_date or id).",
        max_length=30,
        example="title",
    ),
    sort_order: str = Query(
        "asc",
        title="Sort Order",
        description="Sort order (ascending or descending) for results.",
        max_length=4,
        example="desc",
    ),
    skip: int = Query(
        0,
        title="Skip",
        description="Number of records to skip.",
        ge=0,
        example=3,
    ),
    limit: int = Query(
        5,
        title="Limit",
        description="Maximum number of records to return.",
        ge=1,
        le=1000,
        example=10,
    ),
    db: Session = Depends(get_db),
) -> list[models.Book]:
    """
    Retrieve a list of books with pagination (skip, limit), search and sorting functionality.
    """
    books = crud.get_books(
        db=db,
        title=title,
        sort_by=sort_by,
        sort_order=sort_order,
        skip=skip,
        limit=limit,
    )
    return books


@app.get("/authors/{author_id}/books/", response_model=list[schemas.Book])
def read_books_by_author(
    author_id: int, skip: int = 0, limit: int = 5, db: Session = Depends(get_db)
) -> list[models.Book]:
    """
    Filter books by author ID.
    """
    books = crud.get_books_by_author(db, author_id=author_id, skip=skip, limit=limit)
    return books
