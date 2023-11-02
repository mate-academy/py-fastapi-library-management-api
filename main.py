from fastapi import FastAPI, Depends, HTTPException, Query
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
def read_root() -> dict:
    return {"Hello": "World"}


@app.post("/books/", response_model=schemas.BookRetrieve)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@app.get("/books/", response_model=list[schemas.BookList])
def get_all_books(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(5, le=50),
    author_id: int = None,
):
    return crud.get_all_books(db, skip, limit, author_id)


@app.get("/books/{book_id}/", response_model=schemas.BookRetrieve)
def get_single_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_single_book(db, book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.put("/books/{book_id}/", response_model=schemas.BookRetrieve)
def update_single_book(
    book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    db_book = crud.get_single_book(db, book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    crud.update_book(db, book_id, book)

    return crud.get_single_book(db, book_id)


@app.delete("/books/{book_id}/")
def delete_single_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_single_book(db, book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    crud.delete_book(db, book_id)


@app.post("/authors/", response_model=schemas.AuthorRetrieve)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author)


@app.get("/authors/", response_model=list[schemas.AuthorList])
def get_all_authors(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(5, le=50),
):
    return crud.get_all_authors(db, skip, limit)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorRetrieve)
def get_single_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_single_author(db, author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@app.put("/authors/{author_id}/", response_model=schemas.AuthorRetrieve)
def update_single_author(
    author_id: int, author: schemas.AuthorCreate, db: Session = Depends(get_db)
):
    db_author = crud.get_single_author(db, author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    crud.update_author(db, author_id, author)

    return crud.get_single_author(db, author_id)


@app.delete("/authors/{author_id}/")
def delete_single_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_single_author(db, author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    crud.delete_author(db, author_id)
