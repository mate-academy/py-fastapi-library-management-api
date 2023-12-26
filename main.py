from fastapi import FastAPI, Depends, HTTPException
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
def read_authors(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> list[models.Author]:
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author_by_id(author_id: int, db: Session = Depends(get_db)) -> models.Author:
    author = crud.get_author_by_id(author_id=author_id, db=db)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="An author with such name already exists!"
        )
    return crud.create_author(db=db, author=author)


@app.put("/authors/{author_id}/", response_model=schemas.AuthorUpdate)
def update_author(author_id: int, updated_author: schemas.AuthorUpdate, db: Session = Depends(get_db)) -> models.Author:
    return crud.update_author(author_id=author_id, updated_author=updated_author, db=db)


@app.delete("/authors/{author_id}/", response_model=schemas.Author)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author:
        return crud.delete_author(db=db, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        author_id: int | None = None
) -> list[models.Book]:
    if author_id:
        return crud.get_books(db=db, skip=skip, limit=limit, author_id=author_id)
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)) -> models.Book:
    return crud.create_book_with_author(db=db, book=book)


@app.get("/books/{book_id}/", response_model=schemas.Book)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)) -> models.Book:
    return crud.get_book_by_id(book_id=book_id, db=db)


@app.put("/books/{book_id}/", response_model=schemas.Book)
def update_book(
        book_id: int,
        updated_book: schemas.BookUpdate,
        db: Session = Depends(get_db)
) -> models.Book:
    return crud.update_book(book_id=book_id, updated_book=updated_book, db=db)


@app.delete("/books/{book_id}/", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> dict | HTTPException:
    db_book = crud.get_book_by_id(db=db, book_id=book_id)
    if db_book is not None:
        deleted_book = crud.delete_book(book_id=db_book.id, db=db)
        return deleted_book
    else:
        raise HTTPException(status_code=404, detail="Book not found")
