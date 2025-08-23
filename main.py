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


@app.get("/")
def root() -> dict:
    return {"Hello": "World"}


@app.get("/authors/",
         response_model=list[schemas.AuthorBase])
def read_all_authors(skip: int = 0,
                     limit: int = 10,
                     db: Session = Depends(get_db)):
    return crud.get_all_authors(skip=skip,
                                limit=limit, db=db)


@app.post("/authors/",
          response_model=schemas.AuthorBase)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db,
                                        name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/",
         response_model=schemas.AuthorBase)
def read_single_author(author_id: int,
                       db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )
    return db_author


@app.get("/books/", response_model=list[schemas.BookBase])
def read_all_books(
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
):
    return crud.get_book_list(
        author_id=author_id,
        skip=skip,
        limit=limit,
        db=db)


@app.post("/authors/{author_id}/books/",
          response_model=schemas.BookBase)
def create_book_for_author(
        author_id: int,
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    if crud.get_author_by_id(db=db, id=author_id) is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    db_book = crud.create_book_for_author(
        db=db,
        book=book,
        author_id=author_id)
    return db_book


@app.get("/authors/{author_id}/books/",
         response_model=list[schemas.BookBase])
def read_books_by_author_id(
        author_id: int,
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_id(db=db, id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )
    return crud.get_book_by_author_id(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id)
