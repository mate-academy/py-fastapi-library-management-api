from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    return crud.get_all_books(skip=skip, limit=limit, db=db)


@app.get("/books/{author_id}", response_model=list[schemas.Book])
def filter_books(author_id: int, db: Session = Depends(get_db)):
    return crud.get_books_by_author_id(author_id=author_id, db=db)


@app.post("/books/create/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
):
    return crud.create_book(book=book, db=db)


@app.get("/authors/", response_model=list[schemas.Author])
def read_author(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    return crud.get_all_authors(skip=skip, limit=limit, db=db)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def retrieve_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(author_id=author_id, db=db)
    if not author:
        raise HTTPException(
            status_code=400,
            detail=f"Not found author with id: {author_id}"
        )
    return author


@app.post("/authors/create/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
):
    return crud.create_author(author=author, db=db)
