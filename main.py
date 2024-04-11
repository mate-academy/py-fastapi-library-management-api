from fastapi import FastAPI, Depends, HTTPException
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


@app.get("/authors/", response_model=list[schemas.AuthorList])
def read_authors(
        db: Session = Depends(get_db),
        skip: int | None = None,
        limit: int | None = None,
):
    return crud.get_authors_list(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.AuthorList)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="This Author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.AuthorList)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db=db, author_id=author_id)

    if not author:
        raise HTTPException(
            status_code=404,
            detail="Not found"
        )

    return author


@app.get("/books/", response_model=list[schemas.BookList])
def read_books(
        author_id: int | None = None,
        skip: int | None = None,
        limit: int | None = None,
        db: Session = Depends(get_db)
):
    return crud.get_books_list(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit
    )


@app.post("/books/", response_model=schemas.BookList)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
