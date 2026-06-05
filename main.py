from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal, Base, engine


Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Annotated[Session, Depends(get_db)],
        skip: int = 0,
        limit: int = 10
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def retrieve_author(
        author_id: int,
        db: Annotated[Session, Depends(get_db)],
):
    return crud.get_author_by_id(
        db=db,
        author_id=author_id
    )


@app.put("/authors/{author_id}/", response_model=schemas.Author)
def update_author(
        author_id: int,
        author_update_info: schemas.AuthorUpdate,
        db: Annotated[Session, Depends(get_db)]
):
    return crud.update_author(
        db=db,
        author_id_to_update=author_id,
        author_update_info=author_update_info
    )


@app.patch("/authors/{author_id}/", response_model=schemas.Author)
def partial_update_author(
        author_id: int,
        author_update_info: schemas.AuthorPartialUpdate,
        db: Annotated[Session, Depends(get_db)]
):
    return crud.partial_update_author(
        db=db,
        author_id_to_update=author_id,
        author_update_info=author_update_info
    )


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        db: Annotated[Session, Depends(get_db)],
        author_info: schemas.AuthorCreate
):
    return crud.create_author(
        db=db,
        author_info=author_info
    )


@app.delete("/authors/{author_id}/")
def delete_author(
        db: Annotated[Session, Depends(get_db)],
        author_id: int
):
    return crud.delete_author(
        db=db,
        author_id=author_id
    )


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        db: Annotated[Session, Depends(get_db)],
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 10
):
    return crud.get_all_books(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit
    )


@app.get("/books/{book_id}/", response_model=schemas.Book)
def get_book_by_id(
        db: Annotated[Session, Depends(get_db)],
        book_id: int
):
    return crud.get_book_by_id(
        db=db,
        book_id=book_id
    )


@app.post("/books/", response_model=schemas.Book)
def create_book(
        db: Annotated[Session, Depends(get_db)],
        book_info: schemas.BookCreate
):
    return crud.create_book(
        db=db,
        book_info=book_info
    )


@app.put("/books/{book_id}/", response_model=schemas.Book)
def update_book(
        db: Annotated[Session, Depends(get_db)],
        book_id: int,
        book_update_info: schemas.BookUpdate
):
    return crud.update_book(
        db=db,
        book_id=book_id,
        book_update_info=book_update_info
    )


@app.patch("/books/{book_id}/", response_model=schemas.Book)
def partial_update_book(
        db: Annotated[Session, Depends(get_db)],
        book_id: int,
        book_update_info: schemas.BookPartialUpdate
):
    return crud.partial_update_book(
        db=db,
        book_id=book_id,
        book_update_info=book_update_info
    )


@app.delete("/books/{book_id}/", response_model=schemas.Book)
def delete_book(
        db: Annotated[Session, Depends(get_db)],
        book_id: int
):
    return crud.delete_book(
        db=db,
        book_id=book_id
    )
