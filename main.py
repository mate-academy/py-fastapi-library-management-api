import crud
import models
from schemas import Author, Book, BookCreate, AuthorCreate
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[Author])
def get_all_authors(
        skip: int = 0,
        limit: int = 5,
        db: Session = Depends(get_db)
) -> list[Author]:
    authors = crud.get_all_authors(db=db, skip=skip, limit=limit)
    return authors


@app.post("/authors/", response_model=Author)
def create_author(
        author: AuthorCreate,
        db: Session = Depends(get_db)
) -> Author:
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author is not None:
        raise HTTPException(
            status_code=400, detail="Author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=Author)
def get_single_author(
        author_id: int,
        db: Session = Depends(get_db)
) -> Author:
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/books/", response_model=Book)
def create_book(
        book: BookCreate,
        db: Session = Depends(get_db)
) -> Book:
    db_book = crud.get_author_by_id(db=db, author_id=book.author_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Author with this id isn't found")

    return db_book


@app.get("/books/", response_model=list[Book])
def get_all_books(
        author_id: int = None,
        skip: int = 0,
        limit: int = 5,
        db: Session = Depends(get_db)
) -> list[Book]:
    books = crud.get_all_books(
        db=db, skip=skip, limit=limit, author_id=author_id
    )
    return books
