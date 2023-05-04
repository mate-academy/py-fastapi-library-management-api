import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import models
import schemas
from db.engine import SessionLocal
import crud

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "FastAPI"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_author_list(db)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_authors_by_id(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db, author_id)


@app.post("/authors/create/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.create_author(db=db, author=author)
    return db_author


@app.put("authors/{author_id}/update/", response_model=schemas.Author)
def update_author(
        author: schemas.AuthorUpdate,
        author_id: int,
        db: Session = Depends(get_db)
):
    db_author = crud.update_author(author=author, author_id=author_id, db=db)
    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(db: Session = Depends(get_db)):
    return crud.get_book_list(db)


@app.get("/books/{author_id}/", response_model=schemas.Book)
def read_book_by_author_id(author_id: int, db: Session = Depends(get_db)):
    return crud.get_book_by_author_id(db, author_id)


@app.post("/books/create/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    db_book = crud.create_book(db=db, book=book)
    return db_book


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
