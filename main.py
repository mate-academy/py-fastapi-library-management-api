from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root() -> dict:
    return {"Welcome to librariAPI"}


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate, db: Session = Depends(get_db)
) -> schemas.Author:
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[schemas.Author]:
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)) -> schemas.Author:
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate, db: Session = Depends(get_db)
) -> schemas.Book:
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[schemas.Book]:
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/books/author/{author_id}", response_model=List[schemas.Book])
def read_books_by_author(
    author_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[schemas.Book]:
    return crud.get_books_by_author(db=db, author_id=author_id, skip=skip, limit=limit)
