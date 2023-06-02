from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session


import crud
import models
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
def read_authors(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 10
) -> list[models.DBAuthor]:
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.CreateAuthor, db: Session = Depends(get_db)
) -> models.DBAuthor:
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400, detail="Such name for Author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(
    author_id: int, db: Session = Depends(get_db)
) -> models.DBAuthor:
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(7, ge=1, le=10),
) -> list[models.DBBook]:
    return crud.get_book_list(db=db, skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.CreateBook, db: Session = Depends(get_db)
) -> models.DBBook:
    return crud.create_book(db=db, book=book)


@app.get("/books/filter/", response_model=list[schemas.Book])
def read_filter_book_list(
    author_id: int | None = None, db: Session = Depends(get_db)
) -> list[models.DBBook]:
    return crud.get_filter_book_list(db=db, author_id=author_id)
