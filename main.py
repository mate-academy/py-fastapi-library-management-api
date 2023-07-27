from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def greeting_root() -> dict:
    return {"Hello": "Library API is active"}


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
) -> models.Author:

    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with such name already exist"
        )

    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(
        author_id: int,
        db: Session = Depends(get_db),
) -> models.Author:

    db_author = crud.get_author(db, author_id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail=f"Author with id: '{author_id}' not found",
        )

    return db_author


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
) -> list[models.Author]:
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
) -> models.Book:
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
) -> list[models.Book]:
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/books/by_author/{author_id}/", response_model=list[schemas.Book])
def read_filtered_book_list(
        author_id: int | None = None,
        db: Session = Depends(get_db),
) -> list[models.Book]:
    return crud.get_books_list_by_author_id(db=db, author_id=author_id)
