import crud
import schemas

from typing import Annotated
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

from database import get_db, engine, Base


app = FastAPI()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/authors/", response_model=list[schemas.AuthorDto])
def get_authors(
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1)
):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.AuthorDetailDto)
def create_author(
    author: schemas.AuthorCreateUpdateDto,
    db: Annotated[Session, Depends(get_db)]
):
    author_model = crud.create_author(
        author=author,
        db=db
    )
    return author_model


@app.put("/authors/{id}/", response_model=schemas.AuthorDetailDto)
def update_author(
    id: int,
    author: schemas.AuthorCreateUpdateDto,
    db: Annotated[Session, Depends(get_db)]
):
    author_model = crud.update_author(
        id=id,
        author=author,
        db=db
    )
    return author_model


@app.get("/authors/{id}/", response_model=schemas.AuthorDetailDto)
def get_author_by_id(
    id: int,
    db: Annotated[Session, Depends(get_db)]
):
    author = crud.get_author_by_id(
        id=id,
        db=db
    )
    return author


@app.delete("/authors/{id}/", response_model=dict[str, str])
def delete_author(
    id: int,
    db: Annotated[Session, Depends(get_db)]
):
    crud.delete_author(
        id=id,
        db=db
    )
    return {
        "detail": "Author was deleted."
    }


@app.get("/books/", response_model=list[schemas.BookDto])
def get_books(
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    author_id: int | None = Query(None)
):
    return crud.get_books(db=db, skip=skip, limit=limit, author_id=author_id)


@app.post("/books/", response_model=schemas.BookDetailDto)
def create_book(
    book: schemas.BookCreateUpdateDto,
    db: Annotated[Session, Depends(get_db)]
):
    book_model = crud.create_book(
        book=book,
        db=db
    )
    return book_model


@app.put("/books/{id}/", response_model=schemas.BookDetailDto)
def update_book(
    id: int,
    book: schemas.BookCreateUpdateDto,
    db: Annotated[Session, Depends(get_db)]
):
    book_model = crud.update_book(
        id=id,
        book=book,
        db=db
    )
    return book_model


@app.get("/books/{id}/", response_model=schemas.BookDetailDto)
def get_book_by_id(
    id: int,
    db: Annotated[Session, Depends(get_db)]
):
    book = crud.get_book_by_id(
        id=id,
        db=db
    )
    return book


@app.delete("/books/{id}/", response_model=dict[str, str])
def delete_book(
    id: int,
    db: Annotated[Session, Depends(get_db)]
):
    crud.delete_book(
        id=id,
        db=db
    )
    return {
        "detail": "Book was deleted."
    }
