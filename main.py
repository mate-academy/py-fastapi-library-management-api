from typing import Generator, Annotated, List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Library API")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(
    db: Annotated[Session, Depends(get_db)], skip: int = 0, limit: int = 10
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Annotated[Session, Depends(get_db)]):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already registered")
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(
    db: Session = Depends(get_db),
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
):
    return crud.get_all_books(db=db, author_id=author_id, skip=skip, limit=limit)


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.post("/books/", response_model=schemas.Book)
def create_new_book(db_book: schemas.BookCreate, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db=db, author_id=db_book.author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    existing_book = crud.get_book_by_title(db=db, title=db_book.title)
    if existing_book:
        raise HTTPException(
            status_code=400, detail="Book with this title already exists"
        )
    return crud.create_book(db=db, book=db_book)
