from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal, Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        session: Session = Depends(get_db),
        skip: int = 0, limit: int = 10
):
    return crud.get_all_authors(session, skip, limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, session: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(session=session, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="No author")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        session: Session = Depends(get_db)
):
    return crud.create_author(session=session, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        session: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
):
    return crud.get_all_books(session, skip, limit)


@app.get("/authors/{author_id}/books/", response_model=list[schemas.Book])
def read_books_by_author(author_id: int, session: Session = Depends(get_db)):
    db_book = crud.get_book_by_author_id(session=session, author_id=author_id)

    return db_book


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, session: Session = Depends(get_db)):
    book = crud.create_book(session=session, book=book)
    if book is None:
        raise HTTPException(status_code=404, detail="No author")
    return book
