from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal

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
        limit: int = Query(5, ge=0),
        offset: int = Query(0, ge=0)
) -> list[schemas.Author]:
    return crud.get_all_authors(
        db=db,
        limit=limit,
        offset=offset,
    )


@app.post("/authors/", response_model=schemas.Author)
def create_authors(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
) -> schemas.Author:
    db_author = crud.get_author_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=404,
            detail="Such name for Author already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        author_id: int | None = None,
        db: Session = Depends(get_db),
        limit: int = Query(5, ge=0),
        offset: int = Query(0, ge=0)
) -> list[schemas.Book]:
    return crud.get_book_list(
        db=db,
        author_id=author_id,
        limit=limit,
        offset=offset,
    )


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_single_book(
        book_id: int,
        db: Session = Depends(get_db)
) -> schemas.Book:
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return db_book


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
) -> schemas.Book:
    db_book = crud.get_book_by_title(db=db, title=book.title)
    if db_book:
        raise HTTPException(
            status_code=404,
            detail="Such title for Book already exists"
        )

    db_author = crud.get_book_by_author_id(db=db, author_id=book.author_id)
    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return crud.create_book(db=db, book=book)
