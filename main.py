from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import crud
import models  # noqa: F401 - registers models with SQLAlchemy metadata.
import schemas
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


@app.post(
    "/authors",
    response_model=schemas.Author,
    status_code=status.HTTP_201_CREATED,
)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud.create_author(db, author)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An author with this name already exists.",
        )


@app.get("/authors", response_model=list[schemas.Author])
def read_authors(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)

    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found.",
        )

    return author


@app.post(
    "/authors/{author_id}/books",
    response_model=schemas.Book,
    status_code=status.HTTP_201_CREATED,
)
def create_book(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    if crud.get_author(db, author_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found.",
        )

    return crud.create_book(db, book, author_id)


@app.get("/books", response_model=list[schemas.Book])
def read_books(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    author_id: int | None = Query(default=None, ge=1),
    db: Session = Depends(get_db),
):
    return crud.get_books(
        db,
        skip=skip,
        limit=limit,
        author_id=author_id,
    )
