from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/create/", response_model=schemas.AuthorMain)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    author_name = crud.get_autor_by_name(db=db, autor_name=author.name)
    if author_name:
        raise HTTPException(status_code=400, detail="This name already exists")
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.AuthorMain])
def read_authors(limit: int = 50, db: Session = Depends(get_db)):
    authors = crud.get_author_list(db=db, limit=limit)
    return authors


@app.get("/authors/{author_id}/", response_model=schemas.AuthorMain)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db=db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=400, detail="This author does not exist")
    return author


@app.post("/books/create/", response_model=schemas.BookMain)
def create_author(
    book: schemas.BookCreate, author_ids: list[int], db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book, author_ids=author_ids)


@app.get("/books/", response_model=list[schemas.BookMain])
def read_authors(
    limit: int = 50,
    db: Session = Depends(get_db),
):
    books = crud.get_book_list(db=db, limit=limit)
    return books


@app.get("/books/{author_id}/", response_model=list[schemas.BookMain])
def read_authors(
    author_id: int,
    db: Session = Depends(get_db),
):
    books = crud.get_book_list(db=db, author_id=author_id)
    if not books:
        raise HTTPException(status_code=404, detail="Author not found")
    return books
