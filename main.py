from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal

app = FastAPI


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/library/", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db)


@app.post("/library/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such name for Author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/book/", response_model=list[schemas.Book])
def read_book(
        author: str | None = None,
        db: Session = Depends(get_db),
):
    return crud.get_book_list(
        db=db, author=author
    )


@app.get("/book/{book_id}/", response_model=schemas.Book)
def read_single_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.post("/book/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
