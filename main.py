from typing import Generator
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import schemas
from database import SessionLocal, engine, Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.AuthorSchema])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_authors(skip=skip, limit=limit, db=db)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorSchema)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(author_id=author_id, db=db)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/", response_model=schemas.AuthorSchema)
def create_author(author_schema: schemas.AuthorCreateSchema, db: Session = Depends(get_db)):
    return crud.create_author(author_schema=author_schema, db=db)


@app.get("/books/", response_model=list[schemas.BookSchema])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), author_id: int | None = None):
    return crud.get_all_books(skip=skip, limit=limit, author_id=author_id, db=db)


@app.get("/books/{book_id}/", response_model=schemas.BookSchema)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(book_id=book_id, db=db)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/authors/{author_id}/books/", response_model=schemas.BookSchema)
def create_book_for_specific_author(
        author_id: int,
        book_schema: schemas.BookCreateSchema,
        db: Session = Depends(get_db)
):
    author = crud.get_author(author_id=author_id, db=db)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(book_schema=book_schema, author_id=author_id, db=db)


@app.get("/ping")
def ping():
    return {"message": "pong"}
