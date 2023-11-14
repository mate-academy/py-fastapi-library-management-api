from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from db import schemas
from db.engine import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db)


@app.post("/authors/", response_model=list[schemas.Author])
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)):
    author_name = crud.get_author_by_name(db=db, name=author.name)
    if author_name:
        raise HTTPException(
            status_code=400,
            detail="This author is already in our base"
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_detail_author(
        author_id: int,
        db: Session = Depends(get_db)):
    db_author = crud.get_detailed_author(db=db, author_id=author_id)
    if db_author:
        return crud.get_detailed_author(db=db, author_id=author_id)
    raise HTTPException(status_code=400,
                        detail="We haven't such book in base")


@app.get("/books/", response_model=list[schemas.Book])
def read_books(db: Session = Depends(get_db), author_id: int = None, page: int = 0, page_size: int = 20):
    return crud.get_all_books(db=db, author_id=author_id, page=page, page_size=page_size)


@app.post("/books/", response_model=list[schemas.Book])
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)):
    return crud.create_book(db=db, book_data=book)


@app.delete("/books/{book_id}/", response_model=schemas.BookDetail)
def delete_book(
        book_id: int,
        db: Session = Depends(get_db)):
    db_book = crud.get_detailed_book(db=db, book_id=book_id)
    if db_book:
        return crud.delete_book(db=db, book_id=book_id)
    raise HTTPException(status_code=400,
                        detail="We haven't such book in base")


@app.get("/books/{book_id}/", response_model=schemas.BookDetail)
def read_detail_book(
        book_id: int,
        db: Session = Depends(get_db)):
    db_book = crud.get_detailed_book(db=db, book_id=book_id)
    if db_book:
        return crud.get_detailed_book(db=db, book_id=book_id)
    raise HTTPException(status_code=400,
                        detail="We haven't such book in base")