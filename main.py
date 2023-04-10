from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
import crud
from database import SessionLocal

library = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@library.get("/")
def root():
    return {"message": "Hello to Library"}


@library.get(f"/authors/", response_model=list[schemas.AuthorRead])
def read_authors(
        db: Session = Depends(get_db),
        skip: int | None = None,
        limit: int | None = None,
                 ) -> list[schemas.AuthorRead]:
    return crud.get_author_list(db=db, skip=skip, limit=limit)


@library.post("/author-create/", response_model=schemas.AuthorRead)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)) -> schemas.AuthorRead:
    return crud.create_author(author=author, db=db)


@library.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def get_author(
        author_id: int,
        db: Session = Depends(get_db),
) -> HTTPException | schemas.AuthorRead:
    author = crud.get_single_author(db=db, author_id=author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@library.post("/authors/{author_id}/create-book/", response_model=schemas.BookList)
def create_book(author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)) -> schemas.BookList:
    return crud.create_book(db=db, book=book, author_id=author_id)


@library.get("/books/", response_model=list[schemas.BookList])
def get_books(
        db: Session = Depends(get_db),
        author_id: int | None = None,
        skip: int | None = None,
        limit: int | None = None
) -> list[schemas.BookList]:
    return crud.get_book_list(db=db, author_id=author_id, skip=skip, limit=limit)
