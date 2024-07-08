from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

import schemas
import crud
from database import SessionLocal


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello world!"}


@app.get("/books/", response_model=list[schemas.Book])
def get_books(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return crud.get_all_books(db=db, skip=skip, limit=limit)


@app.get("/books/{author_id}/", response_model=list(schemas.Book))
def get_single_book(author_id: int, db: Depends(get_db)):
    db_books = crud.get_all_books(author_id=author_id, db=db)

    if db_books is None:
        raise HTTPException(
            status_code=404,
            detail="Books not found"
        )

    return db_books


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)


@app.get("/authors/", response_model=list(schemas.Author))
def get_authors(
        skip: int | None = 0,
        limit: int | None = 10,
        db: Session = Depends(get_db)
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_single_author_by_id(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such name for author already exists"
        )

    return crud.create_author(db=db, author=author)
