from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import Author, Book
from schemas import (
    AuthorCreate,
    AuthorResponse,
    BookCreate,
    BookResponse,
)
from crud import (
    create_author,
    get_list_of_authors,
    get_author_by_id,
    create_book_by_author,
    get_list_of_books,
    filter_books_by_author_id,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=AuthorResponse)
def create_author_endpoint(
    author: AuthorCreate,
    db: Session = Depends(get_db),
):
    db_author = Author(
        name=author.name,
        bio=author.bio,
    )
    return create_author(db, db_author)


@app.get("/authors/", response_model=list[AuthorResponse])
def get_authors_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_list_of_authors(db, skip, limit)


@app.get("/authors/{author_id}", response_model=AuthorResponse)
def get_author_endpoint(
    author_id: int,
    db: Session = Depends(get_db),
):
    author = get_author_by_id(db, author_id)

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return author


@app.post("/books/", response_model=BookResponse)
def create_book_endpoint(
    book: BookCreate,
    db: Session = Depends(get_db),
):
    author = get_author_by_id(db, book.author_id)

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    db_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )

    return create_book_by_author(db, db_book)


@app.get("/books/", response_model=list[BookResponse])
def get_books_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_list_of_books(db, skip, limit)


@app.get("/books/author/{author_id}", response_model=list[BookResponse])
def get_books_by_author_endpoint(
    author_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return filter_books_by_author_id(
        db,
        author_id,
        skip,
        limit,
    )
