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
def read_authors(
        limit: int = 10,
        offset: int = 10,
        db: Session = Depends(get_db)
):
    return crud.get_all_authors(db=db, limit=limit, offset=offset)


@app.get("/authors/{authors_id}/", response_model=schemas.Author)
def read_single_author(authors_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, authors_id=authors_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
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
            detail="Such name for author already exist"
        )

    return crud.create_author(db=db, author=author)


@app.get("/book/", response_model=list[schemas.Book])
def read_book(
    limit: int = 10,
    offset: int = 0,
    author_id: int | None = None,
    db: Session = Depends(get_db)
):
    return crud.get_book_list(
        db=db, author_id=author_id, limit=limit, offset=offset
    )

@app.get("/book/{book_id}/", response_model=schemas.Book)
def read_single_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return db_book


@app.post("/book/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
