from typing import Annotated, Generator
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas
import crud
from database import SessionLocal

app = FastAPI()


def get_db() -> Generator[Session, None,None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Привіт, Mate Academy!"}

@app.get("/authors", response_model=list[schemas.Author])
def get_authors(db: Annotated[Session, Depends(get_db)],
                skip: int = 0,
                limit: int = 10):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)

@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_single_author(
    db: Annotated[Session, Depends(get_db)],
    author_id: int,
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@app.post("/authors", response_model=schemas.Author)
def create_authors(
    author: schemas.AuthorCreate,
    db: Annotated[Session, Depends(get_db)],
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400, detail="Author with this name already exists"
        )
    return crud.create_author(db=db, author=author)

@app.get("/books", response_model=list[schemas.Book])
def read_book(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
):
    return crud.get_all_books(db=db, skip=skip, limit=limit, author_id=author_id)

@app.get("/books/{book_id}", response_model=schemas.Book)
def read_single_book(
    db: Annotated[Session, Depends(get_db)],
    book_id: int,
):
    db_book = crud. get_book_by_id(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.post("/books", response_model=schemas.Book)
def create_book(
    db: Annotated[Session, Depends(get_db)],
    book: schemas.BookCreate,
):
    db_book = crud.get_book_by_title(db=db, title=book.title)
    if db_book:
        raise HTTPException(
            status_code=400, detail="Book with this title already exists"
        )
    author = crud.get_author_by_id(db=db, author_id=book.author_id)
    if not author:
        raise HTTPException(status_code=400, detail="Author not found")
    return crud.create_book(db=db, book=book)


#uvicorn main:app --reload