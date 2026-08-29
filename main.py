from collections.abc import Generator

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API",
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post(
    "/authors/",
    response_model=schemas.Author,
    status_code=201,
)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    existing_author = crud.get_author_by_name(
        db=db,
        name=author.name,
    )

    if existing_author:
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exists",
        )

    return crud.create_author(
        db=db,
        author=author,
    )


@app.get(
    "/authors/",
    response_model=list[schemas.Author],
)
def get_authors(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1),
    db: Session = Depends(get_db),
):
    return crud.get_authors(
        db=db,
        skip=skip,
        limit=limit,
    )


@app.get(
    "/authors/{author_id}",
    response_model=schemas.Author,
)
def get_author(
    author_id: int,
    db: Session = Depends(get_db),
):
    author = crud.get_author(
        db=db,
        author_id=author_id,
    )

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return author


@app.post(
    "/authors/{author_id}/books/",
    response_model=schemas.Book,
    status_code=201,
)
def create_book(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    author = crud.get_author(
        db=db,
        author_id=author_id,
    )

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return crud.create_book(
        db=db,
        book=book,
        author_id=author_id,
    )


@app.get(
    "/books/",
    response_model=list[schemas.Book],
)
def get_books(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1),
    author_id: int | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_books(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id,
    )
