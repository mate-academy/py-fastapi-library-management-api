from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

import crud
import schemas
from db.engine import SessionLocal


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}


@app.get("/books/")
def read_books(
    author_id: int | None = None, db: Session = Depends(get_db)
) -> Page[schemas.Book]:
    return paginate(crud.get_book_list(db=db, author_id=author_id))


@app.get("/book/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_title(db=db, title=book.title)

    if db_book:
        raise HTTPException(
            status_code=400, detail="Such title for Book already exists"
        )
    return crud.create_book(db=db, book=book)


@app.get("/authors/")
def read_authors(db: Session = Depends(get_db)) -> Page[schemas.Author]:
    return paginate(crud.get_all_authors(db))


@app.get("/author/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400, detail="Such name for Author already exists"
        )
    return crud.create_author(db, author)


add_pagination(app)
