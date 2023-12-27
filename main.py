from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

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
def read_all_authors(db: Session = Depends(get_db),
                     skip: int = 0,
                     limit: int = 5):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{id}", response_model=schemas.Author)
def read_author_by_id(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db=db, author_id=author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate,
                  db: Session = Depends(get_db)):
    author = crud.get_author_by_name(author_name=author.name, db=db)

    if author:
        raise HTTPException(status_code=400,
                            detail="Author already exists")

    return crud.create_author(author=author, db=db)


@app.get("/books/", response_model=list[schemas.Book])
def read_all_books(author_id: int,
                   db: Session = Depends(get_db),
                   skip: int = 0,
                   limit: int = 5):
    return crud.get_all_books(author_id=author_id,
                              db=db,
                              skip=skip,
                              limit=limit)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate,
                db: Session = Depends(get_db)):
    author = crud.get_author_by_id(author_id=book.author_id,
                                   db=db)

    if not author:
        raise HTTPException(status_code=404,
                            detail="Author not found")

    return crud.create_book(db=db, book=book)
