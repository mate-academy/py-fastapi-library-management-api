from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from database import engine, Base, SessionLocal
from models import Author
from schemas import AuthorList, AuthorCreate, BookList, BookCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors", response_model=list[AuthorList])
def get_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return crud.get_all_authors(db, skip, limit)


@app.get("/authors/{author_id}/", response_model=AuthorList)
def get_author(author_id: int, db: Session = Depends(get_db)):
    existing_author = db.query(Author).filter(Author.id == author_id).first()
    if not existing_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.get_author_by_id(author_id, db)


@app.post("/authors", response_model=AuthorList)
def create_author(
        author_data: AuthorCreate,
        db: Session = Depends(get_db),
):
    existing_author = db.query(Author).filter(Author.name == author_data.name).first()
    if existing_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    return existing_author


@app.get("/books/", response_model=list[BookList])
def get_books(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)

):
    return crud.get_alL_book(db, skip, limit)


@app.post("/books/", response_model=BookList)
def create_book(
        book_data: BookCreate,
        db: Session = Depends(get_db),
):
    author = db.query(Author).filter(Author.id == book_data.author_id).first()
    if not author:
        raise HTTPException(status_code=400, detail="Author does not exist")

    return crud.create_book_for_author(db, book_data.author_id, book_data)


@app.get("/authors/{author_id}/books", response_model=list[BookList])
def get_book_author(book_id: int, db: Session = Depends(get_db)):
    return crud.get_books_author(db, book_id)
