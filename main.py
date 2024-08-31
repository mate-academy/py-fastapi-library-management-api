from fastapi import HTTPException

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import schemas
import crud
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def test():
    return {"message": "hello world"}


@app.get("/authors/", response_model=list[schemas.AuthorSchemaList])
def get_author_list(db: Session = Depends(get_db)):
    return crud.get_author_list(db)


@app.post("/authors/", response_model=schemas.AuthorSchemaList)
def create_author(
        author: schemas.AuthorSchemaCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorSchemaList)
def retrieve_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.retrieve_author(db=db, pk=author_id)

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="No author with such id"
        )

    return author


@app.get("/books/", response_model=list[schemas.BookSchemaList])
def get_book_list(db: Session = Depends(get_db)):
    return crud.get_book_list(db)


@app.get("/books/{book_id}/", response_model=schemas.BookSchemaList)
def retrieve_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.retrieve_book(db=db, pk=book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="no book with such id"
        )
    return book


@app.post("/books/", response_model=schemas.BookSchemaList)
def create_book(
        book: schemas.BookSchemaCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)
