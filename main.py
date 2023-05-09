from typing import Any, Generator

from fastapi import Depends, FastAPI, Response, HTTPException, Query

from sqlalchemy.orm import Session

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


def get_or_404(db: Session, model: Any, id: int):
    item = db.query(model).filter(model.id == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return item


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


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)) -> Any:
    """
    Retrieve a single author by ID.
    """
    return get_or_404(db, models.Author, author_id)


@app.put("/authors/{author_id}/", response_model=schemas.Author)
def update_author(
    author_id: int, author: schemas.AuthorUpdate, db: Session = Depends(get_db)
) -> models.Author:
    """
    Update a single author by ID.
    """
    get_or_404(db, models.Author, author_id)
    return crud.update_author(db=db, author=author, author_id=author_id)


@app.delete("/authors/{author_id}/", response_model=schemas.Author)
def delete_author(author_id: int, db: Session = Depends(get_db)) -> Any:
    """
    Delete a single author by ID.
    """
    get_or_404(db, models.Author, author_id)
    crud.delete_author(db=db, author_id=author_id)
    return Response(status_code=204)


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
) -> models.Book:
    """
    Create a new book for a specific author.
    """
    db_author = get_or_404(db, models.Author, author_id)
    return crud.create_book(db=db, book=book, author_id=db_author.id)


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)) -> Any:
    """
    Retrieve a single book by ID.
    """
    return get_or_404(db, models.Book, book_id)


@app.put("/books/{book_id}/", response_model=schemas.Book)
def update_book(
    book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)
) -> models.Book:
    """
    Update a single book by ID.
    """
    get_or_404(db, models.Book, book_id)
    return crud.update_book(db=db, book=book, book_id=book_id)


@app.delete("/books/{book_id}/", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> Any:
    """
    Delete a single book by ID.
    """
    get_or_404(db, models.Book, book_id)
    crud.delete_book(db=db, book_id=book_id)
    return Response(status_code=204)


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
    db_author = get_or_404(db, models.Author, author_id)
    books = crud.get_books_by_author(db, author_id=db_author.id, skip=skip, limit=limit)
    return books
