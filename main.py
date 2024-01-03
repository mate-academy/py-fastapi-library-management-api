from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from db.engine import session
from crud import (get_all_authors,
                  create_author,
                  get_author_by_id,
                  get_all_books,
                  create_book,
                  get_books_by_author_id)
from schemas import Author, AuthorCreate, Book, BookCreate


app = FastAPI()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/", include_in_schema=False)
def get_docs():
    return RedirectResponse(url="/docs")


@app.get("/authors/", response_model=list[Author])
def get_authors(db: Session = Depends(get_db)):
    return get_all_authors(db=db)


@app.post("/authors/", response_model=Author)
def author_create(author: AuthorCreate, db: Session = Depends(get_db)):
    return create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=Author)
def get_by_id_author(author_id, db: Session = Depends(get_db)):
    return get_author_by_id(db=db, author_id=author_id)


@app.get("/books/", response_model=list[Book])
def get_books(db: Session = Depends(get_db)):
    return get_all_books(db=db)


@app.post("/books/", response_model=BookCreate)
def book_create(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db=db, book=book)


@app.get("/books/{author_id}/", response_model=Book)
def books_get_by_author_id(author_id, db: Session = Depends(get_db)):
    return get_books_by_author_id(db=db, author_id=author_id)
