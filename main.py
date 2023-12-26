from fastapi import FastAPI, Depends, HTTPException
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


@app.get("/authors/", response_model=list[schemas.Author])
def read_author(skip: int = 0, limit: int = 2, db: Session = Depends(get_db)) -> dict:
    return crud.get_paginated_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)) -> dict:
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)) -> dict:
    author = crud.get_author_by_id(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


# Update an author by ID
@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author: schemas.AuthorUpdate, db: Session = Depends(get_db)) -> dict:
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.update_author(db=db, db_author=db_author, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_author(skip: int = 0, limit: int = 2, db: Session = Depends(get_db)) -> dict:
    return crud.get_paginated_books(db=db, skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.Book)
def create_book_for_author(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/books/author/{author_id}", response_model=list[schemas.Book])
def read_books_by_author(author_id: int, skip: int = 0, limit: int = 2, db: Session = Depends(get_db)):
    return crud.get_books_by_author_id(db=db, author_id=author_id, skip=skip, limit=limit)
