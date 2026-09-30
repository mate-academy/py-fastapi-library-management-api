from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import Base, SessionLocal, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post(
    "/authors/",
    response_model=schemas.AuthorResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Authors"],
)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author with this name already exists.",
        )
    return crud.create_author(db=db, author=author)


@app.get(
    "/authors/",
    response_model=List[schemas.AuthorResponse],
    tags=["Authors"],
)
def read_authors(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max number of items to return"),
    db: Session = Depends(get_db),
):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get(
    "/authors/{author_id}",
    response_model=schemas.AuthorResponse,
    tags=["Authors"],
)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found.",
        )
    return db_author




@app.post(
    "/authors/{author_id}/books/",
    response_model=schemas.BookResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Books"],
)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found.",
        )
    return crud.create_author_book(db=db, book=book, author_id=author_id)


@app.get(
    "/books/",
    response_model=List[schemas.BookResponse],
    tags=["Books"],
)
def read_books(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max number of items to return"),
    author_id: Optional[int] = Query(None, description="Filter books by Author ID"),
    db: Session = Depends(get_db),
):
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)

