from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import (AuthorBaseSchema,
                     AuthorCreateSchema,
                     BookSchema,
                     BookCreateSchema)
from crud import (get_author,
                  get_author_by_name,
                  get_authors,
                  get_book_by_title,
                  get_books_by_author,
                  get_books,
                  create_author,
                  create_book)


app = FastAPI()


@app.post("/authors/", response_model=AuthorBaseSchema)
def post_author(author: AuthorCreateSchema, db: Session = Depends(get_db)) -> AuthorBaseSchema:
    author_is_exists = get_author_by_name(db, author.name)
    if author_is_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author already exists"
        )

    db_author = create_author(db, author)
    
    return AuthorBaseSchema(name=db_author.name, bio=db_author.bio)


@app.get("/authors/{author_id}", response_model=AuthorBaseSchema)
def retrieve_author(author_id: int, db: Session = Depends(get_db)) -> AuthorBaseSchema:
    db_author = get_author(db, author_id)
    if db_author is None:
        raise  HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    return AuthorBaseSchema(name=db_author.name, bio=db_author.bio)


@app.get("/authors/", response_model=list[AuthorBaseSchema])
def retraieve_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> list[AuthorBaseSchema]:
    authors = get_authors(db, skip, limit)
    if authors.authors is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Authors not found"
        )
    return authors.authors


@app.post("/books/", response_model=BookSchema)
def post_book(book: BookCreateSchema, db: Session = Depends(get_db)) -> BookSchema:
    book_is_exists = get_book_by_title(db, book.title)
    if book_is_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book already exists"
        )
    author = get_author(db, book.author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author not found"
        )
    db_book = create_book(db, book)
    return BookSchema(
        id=db_book.id,
        title=db_book.title,
        summary=db_book.summary,
        published_date=db_book.published_date,
        author=author
    )


@app.get("/books/", response_model=list[BookSchema])
def retrieve_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> list[BookSchema]:
    books = get_books(db, skip, limit)
    if books.books is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Books not found"
        )
    return books.books


@app.get("/books/{author_id}", response_model=list[BookSchema])
def retrieve_book_by_authors(author_id: int, db: Session = Depends(get_db)) -> BookSchema:
    db_author = get_author(db, author_id)
    if db_author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    db_books = get_books_by_author(db, author_id)
    if db_books is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This author don't have any books"
        )
    return db_books.books
