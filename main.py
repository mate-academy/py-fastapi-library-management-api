from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import schemas
import crud
from db.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.AuthorList])
def read_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10),
    db: Session = Depends(get_db)
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorList)
def read_author(
    author_id: int,
    db: Session = Depends(get_db)
):
    author = crud.get_author(db=db, author_id=author_id)

    if author is None:
        raise HTTPException(
            status_code=400,
            detail="No such author!"
        )

    return author


@app.post("/authors/", response_model=schemas.AuthorList)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
):
    if crud.check_author_exists(db=db, author=author):
        raise HTTPException(
            status_code=400,
            detail="Author with such name or bio already exists!"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.BookList])
def read_books(
    author_id: int = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10),
    db: Session = Depends(get_db)
):
    return crud.get_all_books(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit
    )


@app.post("/books/", response_model=schemas.BookList)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    if crud.check_book_exists(db=db, book=book):
        raise HTTPException(
            status_code=400,
            detail="Book with such title or summary already exists!"
        )

    return crud.create_book(db=db, book=book)
