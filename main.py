from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db, Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/authors/", response_model=list[schemas.Author])
def retrieve_authors(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def retrieve_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )
    return db_author


@app.get("/authors/{author_id}/books/", response_model=list[schemas.Book])
def retrieve_author_books(author_id: int, db: Session = Depends(get_db)):
    return crud.get_books(db=db, author_id=author_id)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def retrieve_books(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        author_id: int,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book, author_id=author_id)
