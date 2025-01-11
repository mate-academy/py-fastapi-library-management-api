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
def root():
    return {"message": "Hello"}


@app.get("/authors/", response_model=list[schemas.Author])
def get_all_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db=db)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="The author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/{author_id}/", response_model=schemas.Author)
def update_single_author(
        author_id: int,
        author: schemas.Author,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.update_author(db=db, db_author=db_author, author=author)


@app.delete("/authors/{author_id}/")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    db_author = crud.delete_author(db=db, author_id=author_id)

    return db_author


@app.get("/books/", response_model=list[schemas.BookDetail])
def get_all_books(db: Session = Depends(get_db)):
    return crud.get_all_books(db=db)


@app.post("/books/", response_model=schemas.BookDetail)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    db_book = crud.get_book_by_title(db=db, title=book.title)

    if db_book:
        raise HTTPException(
            status_code=400,
            detail="The book already exists"
        )
    return crud.create_book(db=db, book=book)


@app.get("/books/{book_id}/", response_model=schemas.BookDetail)
def read_single_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db=db, book_id=book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.post("/books/{book_id}/", response_model=schemas.BookDetail)
def update_single_book(
        book_id: int,
        book: schemas.BookDetail,
        db: Session = Depends(get_db)
):
    db_book = crud.get_book(db=db, book_id=book_id)
    author = crud.get_author(db=db, author_id=book.author_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="The book not found")
    elif author is None:
        raise HTTPException(status_code=404, detail="The author not found")
    elif crud.get_book_by_title(db=db, title=book.title):
        raise HTTPException(status_code=409, detail="The book already exists")

    return crud.update_book(db=db, db_book=db_book, book=book)


@app.delete("/books/{book_id}/")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db_book = crud.delete_book(db=db, book_id=book_id)

    return db_book
