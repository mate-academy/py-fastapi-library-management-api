from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0, limit: int = 100
):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{pk}/", response_model=schemas.Author)
def read_single_author(pk: int, db: Session = Depends(get_db)):
    if not crud.get_author(author_id=pk, db=db):
        raise HTTPException(status_code=404, detail="Author not found.")
    return crud.get_author(db=db, author_id=pk)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail=f"Author with name {author.name} already exists!"
        )
    return crud.create_author(db=db, author=author)


@app.get("/books/{author_id}/", response_model=list[schemas.Book])
def read_books(author_id: int | None = None, db: Session = Depends(get_db)):
    return crud.get_books(db=db, author_id=author_id)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=book.author_id)
    if not db_author:
        raise HTTPException(
            status_code=400,
            detail=f"Author with id {book.author_id} does not exist!"
        )
    return crud.create_book(db=db, book=book)
