from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/books/", response_model=list[schemas.BookList])
def read_books(
    skip: int = 0,
    limit: int = 10,
    author_id: int = None,
    db: Session = Depends(get_db),
) -> dict:
    books = crud.get_all_books(
        db=db, author_id=author_id, skip=skip, limit=limit
    )
    return books


@app.post("/books/", response_model=schemas.BookCreate)
def create_book(
    book: schemas.BookCreate, db: Session = Depends(get_db)
) -> dict:
    return crud.create_book(db=db, book=book)


@app.get("/books/{book_id}/", response_model=schemas.BookList)
def read_book(id: int, db: Session = Depends(get_db)) -> dict:
    book = crud.get_book_by_id(book_id=id, db=db)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.get("/authors/", response_model=list[schemas.AuthorList])
def read_authors(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> dict:
    return crud.get_all_authors(skip=skip, limit=limit, db=db)


@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(
    author: schemas.AuthorCreate, db: Session = Depends(get_db)
) -> dict:
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorList)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author
