from fastapi import FastAPI
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from database import SessionLocal
import schemas
import crud

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.AuthorBook])
def read_authors(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such name for Author already exists!"
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorBook)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found!"
        )

    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        skip: int = 0,
        limit: int = 100,
        book_id: str | None = None,
        db: Session = Depends(get_db)
):
    return crud.get_books(db=db, skip=skip, limit=limit, book_id=book_id)


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)
