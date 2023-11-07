from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def authors_list(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def author_retrieve(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/", response_model=schemas.Author)
def author_create(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400, detail="Such name for Author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def books_list(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_books(db, skip, limit)


@app.get("/books/author/{author_id}", response_model=list[schemas.Book])
def books_list_by_author(
    author_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return crud.get_books_by_author(db, author_id, skip, limit)


@app.post("/books/", response_model=schemas.Book)
def book_create(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)
