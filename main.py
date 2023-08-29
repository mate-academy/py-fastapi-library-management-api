from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal, engine


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        database: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(database=database, author_name=author.name)

    if db_author:
        raise HTTPException(status_code=400, detail="Such author already exists")

    return crud.create_author(database=database, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(database: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return crud.get_all_authors(database=database, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_author_by_id(author_id: int, database: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(database=database, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, database: Session = Depends(get_db)):
    return crud.create_book(database=database, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def get_books(database: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return crud.get_all_books(database=database, skip=skip, limit=limit)


@app.get("/books/{author_id}/", response_model=list[schemas.Book])
def get_books_by_author_id(author_id: int, database: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    db_books = crud.get_book_by_author_id(database=database, author_id=author_id, skip=skip, limit=limit)

    if db_books is None:
        raise HTTPException(status_code=404, detail="Books for this author not found")

    return db_books
