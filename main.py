from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session

import schemas
import crud
from database import get_db

app = FastAPI()


def common_pagination_params(
    skip: int = Query(0),
    limit: int = Query(10)
):
    return {"skip": skip, "limit": limit}

CommonsDep = Annotated[dict, Depends(common_pagination_params)]


@app.get("/authors/", response_model=schemas.PaginatedAuthors)
def get_author_list(
    pagination: CommonsDep,
    db: Session = Depends(get_db)
):
    authors = crud.get_authors(db, pagination["skip"], pagination["limit"])
    return schemas.PaginatedAuthors(
        items=authors,
        skip=pagination["skip"],
        limit=pagination["limit"]
    )


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found.")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author is not None:
        raise HTTPException(status_code=400, detail="Author already exists.")

    return crud.create_author(db=db, author=author)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_title(db=db, title=book.title)

    if db_book is not None:
        raise HTTPException(status_code=400, detail="Book already exists.")

    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=schemas.PaginatedBooks)
def get_book_list(
    pagination: CommonsDep,
    db: Session = Depends(get_db),
    author_id: int = Query(None)
):
    books = crud.get_books(
        db=db,
        skip=pagination["skip"],
        limit=pagination["limit"],
        author_id=author_id
    )

    return schemas.PaginatedBooks(
        items=books,
        skip=pagination["skip"],
        limit=pagination["limit"]
    )
