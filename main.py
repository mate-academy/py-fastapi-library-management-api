from fastapi import FastAPI, Depends

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
    return {"Hello": "World"}


@app.get("/authors/", response_model=list[schemas.AuthorRead])
def get_all_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db=db)


@app.get("/books/", response_model=list[schemas.BookRead])
def get_all_books(db: Session = Depends(get_db)):
    return crud.get_all_books(db=db)


@app.post("/books/", response_model=schemas.BookRead)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
