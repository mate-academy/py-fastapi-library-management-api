from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
import schemas
import crud
import models

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello World!"}


@app.get("/author", response_model=list[schemas.Author])
def get_all_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
) -> list[models.DBAuthor]:
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/author/{author_id}", response_model=schemas.Author)
def get_author_by_id(
        author_id: int,
        db: Session = Depends(get_db),
) -> models.DBAuthor:
    db_author = crud.get_author_by_id(db, author_id=author_id)

    if not db_author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return db_author


@app.post("/author", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorBaseCreate,
        db: Session = Depends(get_db),
) -> models.DBAuthor:
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with such name already exist"
        )
    return crud.create_author(db=db, author=author)


@app.get("/book", response_model=list[schemas.Book])
def get_all_books(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> list[models.DBBook]:
    return crud.get_books(db, skip=skip, limit=limit, author_id=None)


@app.get("/book/{author_id}", response_model=list[schemas.Book])
def get_all_author_books_by_author_id(
        author_id: int,
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> list[models.DBBook]:
    return crud.get_books(db=db, skip=skip, limit=limit, author_id=author_id)


@app.post("/book", response_model=schemas.Book)
def create_book(
        book: schemas.BookBaseCreate,
        db: Session = Depends(get_db),
) -> models.DBBook:
    db_author = crud.get_author_by_id(db=db, author_id=book.author_id)

    if not db_author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    db_book = crud.create_book(db=db, book=book)

    return db_book
