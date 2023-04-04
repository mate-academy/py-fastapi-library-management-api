from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import BookService
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/", response_model=dict)
def root() -> dict:
    """Endpoint to test the application"""
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> list[schemas.Author]:
    """Endpoint to retrieve all authors"""
    book_service = BookService(db)
    return book_service.get_all_authors(skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(
        author_id: int,
        db: Session = Depends(get_db)
) -> schemas.Author:
    """Endpoint to retrieve a single author"""
    book_service = BookService(db)
    db_author = book_service.get_author_by_id(author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
) -> schemas.Author:
    """Endpoint to create an author"""
    book_service = BookService(db)
    db_author = book_service.get_author_by_name(name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such name for Author already exists"
        )

    return book_service.create_author(author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        skip: int = 0,
        limit: int = 10,
        author: str | None = None,
        db: Session = Depends(get_db),
) -> list[schemas.Book]:
    """Endpoint to retrieve all books"""
    book_service = BookService(db)
    return book_service.get_book_list(
        skip=skip, limit=limit, author=author
    )


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
) -> schemas.Book:
    """Endpoint to create a book"""
    book_service = BookService(db)
    return book_service.create_book(book=book)
