from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import schemas
import crud
from database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    offset: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    authors = crud.get_authors(offset=offset, limit=limit, db=db)
    return authors


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(name=author.name, db=db)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail=f"Author with name '{author.name}' already exists",
        )
    return crud.create_author(author=author, db=db)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(author_id=author_id, db=db)
    if author is None:
        raise HTTPException(status_code=404, detail="Author is not found")
    return author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    offset: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return crud.get_books(offset=offset, limit=limit, db=db)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(author_id=book.author_id, db=db)
    if author is None:
        raise HTTPException(
            status_code=400,
            detail=f"Author with id {book.author_id} is not found",
        )
    return crud.create_book(book=book, db=db)
