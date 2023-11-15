from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def authors_list(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    authors = crud.get_all_authors(db, skip=skip, limit=limit)
    return authors


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Name must be unique")
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def author_detail(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def books_list(
        skip: int = 0,
        limit: int = 100,
        author_id: int = None,
        db: Session = Depends(get_db)
):
    books = crud.get_all_books(
        db,
        skip=skip,
        limit=limit,
        author_id=author_id
    )
    return books


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
