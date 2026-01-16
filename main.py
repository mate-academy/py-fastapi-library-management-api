from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db, Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 4
):

    return crud.get_authors_list(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exists in the database"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        author_id: int | None = None,
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 4
):

    return crud.get_books_list(db=db, author_id=author_id, skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=book.author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author does not exist in the database"
        )

    return crud.create_book(db=db, book=book)
