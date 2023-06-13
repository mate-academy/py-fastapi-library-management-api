from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal

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
        skip: int = 0,
        limit: int = 10
):
    return crud.get_all_authors(
        db=db,
        skip=skip,
        limit=limit
    )


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def retrieve_single_author_by_id(
        author_id: int,
        db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author is not found"
        )

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such name for author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        author_id: int | None = None,
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
):
    return crud.get_book_list(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit
    )


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
):

    return crud.create_book(db=db, book=book)
