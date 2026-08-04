from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud

from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)

    if authors is None:
        raise HTTPException(status_code=404, detail="Authors not found")

    return authors


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(author_id: int,
                            book: schemas.BookCreate,
                              db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        skip: int = 0,
          limit: int = 10,
          author_id: int | None = None,
      db: Session = Depends(get_db)
):
    if author_id:
        return crud.get_books_by_author(db, author_id=author_id)
    return crud.get_books(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(
    author_id: int,
    db: Session = Depends(get_db)
):
    author = crud.get_author(db, author_id)

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return author
