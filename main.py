from typing import Annotated, Generator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import models
from engine import SessionLocal, engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine) 

def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Welcome to your own library"}


@app.get("/authors/", response_model=list[schemas.Author]) # with pagination
def get_all_authors(db: Annotated[Session, Depends(get_db)], skip: int = 0, limit: int = 10):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/author/{author_id}/", response_model=schemas.Author) # Retrieve a single author by ID.
def get_autor_by_id(
    author_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/author/", response_model=schemas.Author) # Create a new author.
def create_author(
        author : schemas.CreateAuthor,
        db: Annotated[Session, Depends(get_db)]
):
    author_name = db.query(models.DBAuthor).filter(models.DBAuthor.name == author.name).first()

    if author_name:
        raise HTTPException(status_code=409, detail="Author with this name already exists")
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book]) # should be with pagination
def get_all_books(db: Annotated[Session, Depends(get_db)], skip: int = 0, limit: int = 10):
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/book_by_author_id/{author_id}/", response_model=list[schemas.Book]) # done
def get_book_by_author_id(
    author_id: int,
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 10
):
    db_book = crud.get_book_by_author_id(db=db, author_id=author_id, skip=skip, limit=limit)

    if not db_book:
        raise HTTPException(status_code=404, detail="No books for this author")

    return db_book


@app.post("/book/", response_model=schemas.Book) # Create a new book. Func should check if such author is existing
def create_book(
        book : schemas.CreateBook,
        db: Annotated[Session, Depends(get_db)]
):
    try:
        return crud.create_book(db=db, book=book)
    except ValueError:
        raise HTTPException(status_code=404, detail="invalid author id")
