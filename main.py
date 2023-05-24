from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
from db.engine import SessionLocal
from schemas import AuthorBase, BookBase

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


@app.get("/authors/", response_model=list[AuthorBase])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_all_author(db)


@app.get("/books/", response_model=list[BookBase])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_all_books(db)
