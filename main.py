from fastapi import FastAPI, Depends

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> SessionLocal:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(db: SessionLocal = Depends(get_db)):
    return crud.get_authors(db)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: SessionLocal = Depends(get_db)):
    return crud.get_single_author(author_id=author_id, db=db)


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: SessionLocal = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=schemas.Book)
def get_books(db: SessionLocal = Depends(get_db)):
    return crud.get_books(db=db)


@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: SessionLocal = Depends(get_db)):
    return crud.get_single_book(book_id=book_id, db=db)


@app.get("/books/authors/{author_id}", response_model=schemas.Book)
def get_books_by_author(author_id: int, db: SessionLocal = Depends(get_db)):
    return crud.get_books_by_author(db=db, author_id=author_id)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: SessionLocal = Depends(get_db)):
    return crud.create_book(book=book, db=db)
