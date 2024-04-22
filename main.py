from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import (
    get_book_list,
    get_author_by_name,
    create_book,
    create_author, get_author_list, get_author_detail, get_book_detail,
)
from db.models import DbAuthor, DbBook

from schemas import (
    Author, AuthorCreate, Book, BookCreate
)
from db.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    print("Received request at root endpoint")
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[Author])
def read_authors(
        db: Session = Depends(get_db)
) -> list[DbAuthor]:
    return get_author_list(db=db)


@app.get("/authors/{author_id}/", response_model=Author)
def read_single_author(
        author_id: int, db: Session = Depends(get_db)
) -> DbAuthor:
    db_author = get_author_detail(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=Author)
def create_author_endpoint(
    author: AuthorCreate,
    db: Session = Depends(get_db),
) -> DbAuthor:
    db_author = get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="This author already exists"
        )

    return create_author(db=db, author=author)


@app.get("/books/", response_model=list[Book])
def read_books(
    author_id: int | None = None,
    author_name: str | None = None,
    db: Session = Depends(get_db),
) -> list[DbBook]:
    return get_book_list(
        db=db,
        author_id=author_id,
        author_name=author_name,
    )


@app.get("/books/{book_id}/", response_model=Book)
def read_single_book(
        book_id: int, db: Session = Depends(get_db)
) -> DbBook:
    db_book = get_book_detail(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.post("/books/", response_model=Book)
def create_book_endpoint(
        book: BookCreate, db: Session = Depends(get_db)
) -> DbBook:
    return create_book(db=db, book=book)
