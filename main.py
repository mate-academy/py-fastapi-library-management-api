from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(author_id: int, book: schemas.BookCreate,
                           db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, author_id: int = None,
               db: Session = Depends(get_db)):
    return crud.get_books(db=db, skip=skip, limit=limit, author_id=author_id)
