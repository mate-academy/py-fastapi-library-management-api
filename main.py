from fastapi import FastAPI, HTTPException, Query
from fastapi.params import Depends
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def get_all_authors(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1),
        db: Session = Depends(get_db),
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db=db, author_id=author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def get_all_books(db: Session = Depends(get_db),
                  skip: int = Query(0, ge=0),
                  limit: int = Query(100, ge=1),
                  author_id: int | None = None):
    if author_id:
        author = crud.get_author(db=db, author_id=author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
    return crud.get_all_books(db=db,
                              author_id=author_id,
                              skip=skip,
                              limit=limit)


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)
