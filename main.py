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



@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Session = Depends(get_db),
        limit: int | None = None,
        skip: int | None = None,

):
    return crud.get_all_authors(db=db, limit=limit, skip=skip)


@app.post("/authors/", response_model=schemas.Author)
def create_authors(
        authors: schemas.AuthorCreate,
        db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=authors.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="This name for Author already exists"
        )

    return crud.create_author(db=db, author=authors)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        db: Session = Depends(get_db),
        limit: int | None = None,
        skip: int | None = None,
        author_id: int | None = None,
):
    return crud.get_book_list(
        db=db, limit=limit, skip=skip, author_id=author_id
    )


@app.get("/books/{book_id}", response_model=schemas.Book)
def detail_book(
        book_id: int, db: Session = Depends(get_db),
):
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=400, detail="Book not found")

    return db_book


@app.get("/authors/{author_id}", response_model=schemas.Author)
def detail_author(
        author_id: int, db: Session = Depends(get_db)
):
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=400, detail="Author not found")

    return db_author


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate, db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)
