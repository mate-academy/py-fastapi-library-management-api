from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Session = Depends(get_db),
        offset: int = 0,
        limit: int = Query(default=10, lte=100)
) -> list[schemas.Author]:
    return crud.get_authors_list(db=db, offset=offset, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(
        author_id: int,
        db: Session = Depends(get_db)
) -> HTTPException | schemas.Author:
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> HTTPException | schemas.Author:
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        author_id: int | None = None,
        db: Session = Depends(get_db),
        offset: int = 0,
        limit: int = Query(default=10, lte=100)
) -> list[schemas.Book]:
    return crud.get_books_list(
        db=db,
        author_id=author_id,
        offset=offset,
        limit=limit
    )


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.Book:
    db_author = crud.get_author(db=db, author_id=book.author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_book(db=db, book=book)
