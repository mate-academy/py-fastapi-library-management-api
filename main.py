from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import schemas
from data_base.database import SessionLocal

app = FastAPI()


def get_data_base() -> Session:
    data_base = SessionLocal()

    try:
        yield data_base
    finally:
        data_base.close()


@app.get("/")
def root() -> dict:
    return {"message": "Bang Bang"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        data_base: Session = Depends(get_data_base),
        page: int = Query(ge=0, default=0),
        size: int = Query(ge=1, le=100)
) -> list:
    return crud.get_all_authors(data_base, page, size)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    data_base: Session = Depends(get_data_base)
):
    data_base_author = crud.get_author_by_name(data_base=data_base, name=author.name)

    if data_base_author:
        raise HTTPException(
            status_code=400,
            detail="Name already exist"
        )

    return crud.create_author(data_base=data_base, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, data_base: Session = Depends(get_data_base)):
    data_base_author = crud.get_author(data_base=data_base, author_id=author_id)

    if data_base_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return data_base_author


@app.delete("/authors/{author_id}/", response_model=bool)
def delete_single_author(author_id: int, data_base: Session = Depends(get_data_base)):
    deleted = crud.delete_author(data_base=data_base, author_id=author_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Author not found")
    return True


@app.get("/books/", response_model=list[schemas.Book])
def get_all_books(
    data_base: Session = Depends(get_data_base),
    author_id: int | None = None,
    page: int = Query(ge=0, default=0),
    size: int = Query(ge=1, le=100)
):
    return crud.get_all_books(
        data_base=data_base, author_id=author_id, page=page, size=size
    )


@app.get("/books/book_id/", response_model=schemas.Book)
def read_single_book(book_id: int, data_base: Session = Depends(get_data_base)):
    data_base_book = crud.get_book(data_base=data_base, book_id=book_id)

    if data_base_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return data_base_book


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, data_base: Session = Depends(get_data_base)):
    return crud.create_book(data_base=data_base, book=book)


@app.delete("/books/{book_id}/", response_model=bool)
def delete_single_book(book_id: int, data_base: Session = Depends(get_data_base)):
    deleted = crud.delete_book(data_base=data_base, book_id=book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return True
