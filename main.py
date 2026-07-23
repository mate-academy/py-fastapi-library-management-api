from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


@app.post(
    "/author/",
    response_model=schemas.Author,
)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.create_author(db=db, author=author)
    return db_author


@app.get("/authors_list/", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db), skip: int = 0, limit: int = 5):
    return crud.get_list_authors(db=db, skip=skip, limit=limit)


@app.get("/author/{author_id}/", response_model=schemas.Author)
def read_single_author(
    author_id: int,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/book/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=book.author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    db_book = crud.create_book_for_author(db=db, book=book)
    return db_book


@app.get("/books_list/", response_model=list[schemas.Book])
def read_books(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 5,
    author_id: int | None = None,
):
    return crud.get_books_list(
        db=db, skip=skip, limit=limit, author_id=author_id
    )
