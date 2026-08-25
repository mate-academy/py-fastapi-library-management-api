from fastapi import HTTPException

from fastapi import FastAPI, Depends
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


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    return crud.get_all_books(db=db, skip=skip, limit=limit)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    return crud.get_all_authors(skip=skip, limit=limit, db=db)


@app.post("/create_authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author already exists",
        )

    return crud.create_author(db=db, author=author)


@app.get("/book/", response_model=list[schemas.Book])
def read_books_list(
        title: str | None = None,
        author_id: int | None = None,
        db: Session = Depends(get_db)
):
    return crud.get_book_list(db=db, author_id=author_id, title=title)


@app.get("/author/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return db_author


@app.get("/book/{book_id}/", response_model=schemas.Book)
def read_single_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    return db_book


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
        author_id: int,
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    db_book = crud.get_book_by_title(db=db, book_name=book.title)
    if db_book:
        raise HTTPException(
            status_code=400,
            detail="Book already exists",
        )

    return crud.create_book(db=db, book=book, author_id=author_id)
