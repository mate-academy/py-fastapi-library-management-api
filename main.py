from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

import schemas
import crud
from db.database import Sessionlocal
from db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db() -> Session:
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
):
    return crud.get_all_authors(
        db=db,
        skip=skip,
        limit=limit
    )


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_single_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    db_author = crud.get_single_author_by_id(
        db=db,
        author_id=author_id
    )
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author

@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author =  crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with such name already exists"
        )

    return crud.create_author(db=db, author=author)

@app.get("/books/", response_model=list[schemas.Book])
def get_books(
        db: Session = Depends(get_db),
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 10
):
    return crud.get_book_list(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit
    )


@app.get("/books/{book_id}/", response_model=schemas.Book)
def get_single_book(
        book_id: int,
        db: Session = Depends(get_db)
):
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):

    return crud.create_book(db=db, book=book)
