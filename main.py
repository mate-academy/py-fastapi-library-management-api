from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
import crud
import schemas
from database import SessionLocal, Base, engine
import models

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)

@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db=db, author_id=author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.get_authors_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author with this name already exists")

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, author_id: int | None = None, db: Session = Depends(get_db)):
    return crud.get_all_books(db=db, author_id=author_id, skip=skip, limit=limit)


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db=db, book_id=book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    return crud.create_book(db=db, book=book, author_id=author_id)