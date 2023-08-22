from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from library.database import SessionLocal
from library import crud, schemas


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def post_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.post_author(
        db=db,
        author=author
    )


@app.get("/authors/", response_model=List[schemas.Author])
def get_authors(
        skip: int = 0,
        limit: int = 0,
        db: Session = Depends(get_db)
):
    return crud.get_authors(
        db=db,
        skip=skip,
        limit=limit
    )


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_author_by_id(
        author_id: int,
        db: Session = Depends(get_db)
):
    author = crud.get_author_by_id(
        db=db,
        author_id=author_id
    )

    if not author:
        raise HTTPException(status_code=404, detail="Author doesn't exist")


@app.post("/books/", response_model=schemas.Book)
def post_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    author = crud.get_author_by_id(db=db, author_id=book.author_id)

    if not author:
        raise HTTPException(
            status_code=400,
            detail="Author doesn't exist"
        )
    return crud.post_book(
        book=book,
        db=db
    )


@app.get("/books/", response_model=List[schemas.Book])
def get_books(
        skip: int = 0,
        limit: int = 0,
        db: Session = Depends(get_db)
):
    return crud.get_books(
        skip=skip,
        limit=limit,
        db=db
    )


@app.get("/books/{author_id}/")
def get_books_by_author_id(
        author_id: int,
        skip: int = 0,
        limit: int = 0,
        db: Session = Depends(get_db)
):

    books = crud.get_books_by_author_id(
        skip=skip,
        limit=limit,
        author_id=author_id,
        db=db
    )

    if not books:
        raise HTTPException(
            status_code=404,
            detail="No books found for this author"
        )
    return books
