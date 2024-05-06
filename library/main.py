from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from library import schemas, crud
from library.database import SessionLocal


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Authors": "/authors", "Books": "/books"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: int = 0, limit: int = 2, db: Session = Depends(get_db)
) -> list[schemas.Author]:
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(
    author_id: int, db: Session = Depends(get_db)
) -> schemas.Author:
    db_user = crud.get_author_by_id(db=db, author_id=author_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_user


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate, db: Session = Depends(get_db)
) -> schemas.Author:
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 2,
    author_id: int | None = None,
    db: Session = Depends(get_db),
) -> list[schemas.Book]:
    return crud.get_books(db=db, skip=skip, limit=limit, author_id=author_id)


@app.post("/books/", response_model=schemas.Book)
def create_books(
    book: schemas.BookCreate, db: Session = Depends(get_db)
) -> schemas.Book:
    return crud.create_book(db=db, book=book)
