from fastapi import HTTPException

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors", response_model=list[schemas.AuthorListSchema])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10,
):
    return crud.get_all_authors(db=db,)


@app.get("/authors/{author_id}", response_model=schemas.AuthorListSchema)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(author_id=author_id, db=db)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors", response_model=schemas.AuthorCreateSchema)
def create_author(author: schemas.AuthorCreateSchema, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(author_name=author.name, db=db)

    if db_author:
        raise HTTPException(status_code=400, detail="Author with this name already exist")

    return crud.create_author(author=author, db=db)


@app.get("/books", response_model=list[schemas.BookListSchema])
def read_books(
        db: Session = Depends(get_db),
        author_id: int = None,
        skip: int = 0,
        limit: int = 10,
):
    return crud.get_all_books(db=db, author_id=author_id)


@app.get("/books/{book_id}", response_model=schemas.BookListSchema)
def read_single_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(book_id=book_id, db=db)

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.post("/books", response_model=schemas.BookCreateSchema)
def create_book(book: schemas.BookCreateSchema, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(author_id=book.author_id, db=db)

    if not db_author:
        raise HTTPException(status_code=400, detail="Author with this id does not exist")

    return crud.create_book(book=book, db=db)
