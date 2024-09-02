from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal
from models import DBAuthor, DBBook

app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/author/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)) -> DBAuthor:
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such name for Author already exist"
        )

    return crud.create_author(db=db, author=author)


@app.get("/author/", response_model=list[schemas.Author])
def read_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> [DBAuthor]:
    authors = crud.get_author_list(db=db, skip=skip, limit=limit)
    return authors


@app.get("/author/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)) -> DBAuthor:
    return crud.get_author_retrieve(db=db, author_id=author_id)


@app.post("/book/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)) -> DBBook:
    return crud.create_book(db=db, book=book)


@app.get("/book/", response_model=list[schemas.Book])
def read_books(
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None,
        db: Session = Depends(get_db)
) -> [DBBook]:
    books = crud.get_book_list(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit
    )
    return books


@app.get("/book/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)) -> DBBook:
    return crud.get_book_retrieve(db=db, book_id=book_id)
