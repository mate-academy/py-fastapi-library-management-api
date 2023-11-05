from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


@app.get("/")
def root() -> dict:
    return {"info": "Test Page"}


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        limit: int = 10,
        offset: int = 0,
        db: Session = Depends(get_db)
):

    return crud.get_all_authors(db=db, limit=limit, offset=offset)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author is not None:
        raise HTTPException(
            status_code=400,
            detail="Such name for Author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def retrieve_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author does not exist"
        )

    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    limit: int = 10,
    offset: int = 0,
    author_id: int | None = None,
    db: Session = Depends(get_db)
):
    return crud.get_book_list(
        db=db,
        author_id=author_id,
        limit=limit,
        offset=offset
    )


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)
