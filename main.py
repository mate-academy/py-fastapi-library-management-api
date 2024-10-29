from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from crud import create_author, get_all_authors, get_author_by_name, get_book_list, get_author, create_book
from database import SessionLocal
from schemas import Author, AuthorCreate, Book, BookCreate

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
):
    return get_all_authors(db=db)[skip: skip + limit]


@app.get("/authors/{author_id}/", response_model=Author)
def read_book(author_id: int, db: Session = Depends(get_db)):
    db_author = get_author(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exists"
        )

    return create_author(db=db, author=author)


@app.get("/books/", response_model=list[Book])
def read_books(
        author_id: int | None = None,
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
):
    return get_book_list(db=db, author_id=author_id)[skip: skip + limit]

@app.post("/books/", response_model=Book)
def create_book_endpoint(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db=db, book=book)
