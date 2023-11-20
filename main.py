from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

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
def read_root():
    return {"message": "API Root"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
):
    return crud.get_author_list(db)[skip : skip + limit]


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.get_author(db, author_id)


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db, name=author.name)

    if db_author:
        raise HTTPException(status_code=400, detail=f"{author.name} already exists")

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    db: Session = Depends(get_db),
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
):
    return crud.get_book_list(db=db, author_id=author_id)[skip : skip + limit]


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return crud.get_book(db, book_id)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
