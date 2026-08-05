from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal, Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
):
    return crud.get_all_authors(db, skip, limit)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        author_id: int | None = None,
):
    return crud.get_all_books(db, skip, limit, author_id)


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    db_book = crud.get_book_by_title(db, title=book.title)

    author = crud.get_author(db, author_id=book.author_id)

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    if db_book:
        raise HTTPException(
            status_code=400,
            detail="Book with this title already exists"
        )

    return crud.create_book(db, book=book)

@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db, author=author)

@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    author = crud.get_author(db, author_id=author_id)

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )
    return author
