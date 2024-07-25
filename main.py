from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/get-all-books/", response_model=list[schemas.BookList])
def get_all_books(db: Session = Depends(get_db)) -> list:
    return crud.get_all_books(db)


@app.get("/retrieve-book/{book_id}/", response_model=schemas.BookList)
def retrieve_book(db: Session = Depends(get_db), book_id: int = None) -> list:
    return crud.retrieve_book(db, book_id)


@app.post("/create-book/", response_model=schemas.BookBase)
def create_book(db: Session = Depends(get_db), book: schemas.BookBase = None) -> dict:
    return crud.create_book(db, book)


@app.delete("/delete-book/{book_id}/", response_model=dict)
def delete_book(db: Session = Depends(get_db), book_id: int = None) -> dict:
    return crud.delete_book(db, book_id)


@app.get("/get-all-authors/", response_model=list[schemas.AuthorList])
def get_all_authors(db: Session = Depends(get_db)) -> list:
    return crud.get_all_authors(db)


@app.get("/retrieve-author/{author_id}/", response_model=schemas.AuthorList)
def retrieve_author(db: Session = Depends(get_db), author_id: int = None) -> list:
    return crud.retrieve_author(db, author_id)


@app.post("/create-author/", response_model=schemas.AuthorBase)
def create_author(db: Session = Depends(get_db), author: schemas.AuthorBase = None) -> dict:
    return crud.create_author(db, author)


@app.delete("/delete-author/{author_id}/", response_model=dict)
def delete_author(db: Session = Depends(get_db), author_id: int = None) -> dict:
    return crud.delete_author(db, author_id)
