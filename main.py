from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=50),
) -> list[schemas.Author]:

    return crud.get_all_author(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(
        author_id: int,
        db: Session = Depends(get_db)
) -> schemas.Author:

    author = crud.get_author(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
) -> schemas.Author:

    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author is None:
        return crud.create_author(db=db, author=author)
    raise HTTPException(status_code=400, detail="Author exist")


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=50),
        db: Session = Depends(get_db),
        author_id: int | None = None,
) -> list[schemas.Book]:

    return crud.get_all_book(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit
    )


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
) -> schemas.Book:

    author = crud.get_author(db=db, author_id=book.author_id)
    if author is not None:
        return crud.create_book(db=db, book=book)
    raise HTTPException(status_code=400, detail="Author doesn`t exist or else")
