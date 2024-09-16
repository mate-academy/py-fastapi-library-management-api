from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


@app.post("/create_author/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
) -> schemas.Author:
    new_author = crud.create_author(db=db, author=author)

    return new_author


@app.get("/authors/", response_model=list[schemas.Author])
def list_authors(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=50),
) -> list[schemas.Author]:
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def retrieve_author(
        author_id: int,
        db: Session = Depends(get_db),
) -> schemas.Author:
    db_author = crud.get_author_by_id(db, author_id=author_id)

    return db_author


@app.put("/authors/{author_id}/", response_model=schemas.Author)
def update_author(
    author_id: int,
    author: schemas.AuthorUpdate,
    db: Session = Depends(get_db),
) -> schemas.Author:
    author = crud.update_author(db=db, author_id=author_id, author=author)

    return author


@app.delete("/authors/{author_id}/")
def delete_author(author_id: int, db: Session = Depends(get_db)) -> dict:
    crud.delete_author(db=db, author_id=author_id)

    return {"message": "Author deleted"}


@app.get("/books/", response_model=list[schemas.Book])
def list_books(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=50),
) -> list[schemas.Book]:
    return crud.get_all_books(db=db, skip=skip, limit=limit)


@app.post("/create_book/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
) -> schemas.Book:
    new_book = crud.create_book(db=db, book=book)

    return new_book


@app.get("/books/{book_title}/", response_model=schemas.Book)
def retrieve_book(
        book_id: int,
        db: Session = Depends(get_db),
) -> schemas.Book:
    db_book = crud.get_book_by_id(db, book_id=book_id)

    return db_book


@app.put("/books/{book_id}/", response_model=schemas.Book)
def update_book(
    book_id: int,
    book: schemas.BookUpdate,
    db: Session = Depends(get_db),
) -> schemas.Book:
    book = crud.update_book(db=db, book_id=book_id, book=book)

    return book


@app.delete("/books/{book_id}/")
def delete_book(book_id: int, db: Session = Depends(get_db)) -> dict:
    crud.delete_book(db=db, book_id=book_id)

    return {"message": "Book deleted"}
