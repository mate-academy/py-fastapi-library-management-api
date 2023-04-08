from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
import crud, schemas
from library import models
from library.engine import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/books/", response_model=list[schemas.BookList])
def read_books(db: Session = Depends(get_db)):
    return crud.get_all_books(db=db)


@app.post("/books/", response_model=list[schemas.BookList])
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)


@app.get("/authors/", response_model=list[schemas.AuthorList])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db=db)


@app.post("/authors/", response_model=list[schemas.AuthorList])
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)
