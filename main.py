from typing import List

from fastapi import (
    FastAPI,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session

import crud
from database import (
    SessionLocal,
    Base,
    engine
)
from schemas import (
    Author,
    Book,
    AuthorBaseCreate,
    BookBaseCreate
)


app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get(
    "/authors/",
    response_model=List[Author]
)
def get_all_authors_with_pagination(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
):
    return crud.get_authors_with_pagination(
        db=db,
        skip=skip,
        limit=limit
    )


@app.get(
    "/authors/{author_id}/",
    response_model=Author
)
def get_one_author_by_id(
        author_id: int,
        db: Session = Depends(get_db),
):
    return crud.get_author_by_id_or_404(
        db=db,
        author_id=author_id
    )


@app.post(
    "/authors/",
    response_model=Author
)
def create_new_author(
        author: AuthorBaseCreate,
        db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(
        db=db, author_name=author.name
    )
    if db_author:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Author (name: {db_author.name})"
                f" already exists"
            )
        )
    return crud.create_author(
        db=db,
        new_author=author
    )


@app.get(
    "/books/",
    response_model=List[Book]
)
def get_all_books_with_pagination(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
):
    return crud.get_books_with_pagination(
        db=db,
        skip=skip,
        limit=limit
    )


@app.post(
    "/authors/{author_id}/books/",
    response_model=Book
)
def create_new_author_book(
        author_id: int,
        book: BookBaseCreate,
        db: Session = Depends(get_db),
):
    crud.get_author_by_id_or_404(
        db=db,
        author_id=author_id
    )

    return crud.create_book(
        db=db,
        new_book=book,
        author_id=author_id
    )


@app.get(
    "/authors/{author_id}/books/",
    response_model=List[Book]
)
def get_books_filtered_by_author_id(
        author_id: int,
        db: Session = Depends(get_db)
):
    crud.get_author_by_id_or_404(
        db=db,
        author_id=author_id
    )

    return crud.filter_books_by_author_id(
        db=db,
        author_id=author_id
    )
