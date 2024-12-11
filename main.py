from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


# Retrieve a list of authors with pagination
@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(5, gt=0),
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


# Retrieve a single author by ID
@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db=db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


# Create a new author
@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such name for Author already exists"
        )

    return crud.create_author(db=db, author=author)


# Retrieve a list of books with pagination
@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        skip: int,
        limit: int,
        author_id: int = None,
        db: Session = Depends(get_db)
):
    return crud.get_all_books(
        db=db, skip=skip, limit=limit, author_id=author_id
    )


@app.post("/authors/{author_id}/", response_model=schemas.Book)
def create_book_for_author(
        author_id: int,
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
):
    author = crud.get_author_by_id(db=db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, book=book)
