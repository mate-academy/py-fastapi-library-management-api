from fastapi import FastAPI, Depends, HTTPException
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


@app.get("/books", response_model=list[schemas.Book])
def read_books(
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None,
        db: Session = Depends(get_db)
) -> list[schemas.Book]:
    return crud.get_all_books(
        db,
        skip=skip,
        limit=limit,
        author_id=author_id
    )

@app.get("/authors", response_model=list[schemas.Author])
def read_authors(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(
    author_id: int,
    db: Session = Depends(get_db),
):
    author = crud.get_author(db, author_id=author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return author

@app.post("/authors", response_model=schemas.Author, status_code=201)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    return crud.create_author(db, author=author)


@app.post(
    "/authors/{author_id}/books",
    response_model=schemas.Book,
    status_code=201,
)
def create_book(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    author = crud.get_author(db, author_id=author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_book(db, book=book, author_id=author_id)
