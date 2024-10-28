from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal
from models import DBAuthor

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author_by_id(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, author_name=author.name)

    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(db=db, author=author)


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book(
        author_id: int,
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    db_author = db.query(DBAuthor).filter(DBAuthor.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/books/author/{author_id}/", response_model=list[schemas.Book])
def read_book_by_author(author_id: int, db: Session = Depends(get_db)):
    db_books = crud.get_books_by_author(db=db, author_id=author_id)

    if not db_books:
        raise HTTPException(
            status_code=404,
            detail="Books not found for this author"
        )

    return db_books
