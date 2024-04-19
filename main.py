from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from db.database import SessionLocal
from schemas import Author, Book, AuthorCreate, BookCreate

app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10,
):
    return crud.get_all_authors(
        db,
        skip=skip,
        limit=limit,
    )


@app.get(
    "/authors/{author_id}/",
    response_model=Author
)
def read_author_detail(
        author_id: int,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author(
        db=db,
        author_id=author_id
    )

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return db_author


@app.post("/authors/", response_model=Author)
def create_author(
        author: AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(
        db=db,
        name=author.name
    )

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[Book])
def read_books(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10,
):
    return crud.get_all_books(
        db=db,
        skip=skip,
        limit=limit
    )


@app.get("/books/{book_id}/", response_model=Book)
def read_book_detail(
        book_id: int,
        db: Session = Depends(get_db)
):
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return db_book


@app.post("/books/", response_model=Book)
def create_book(
        book: BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)
