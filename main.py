from fastapi import FastAPI, Depends, HTTPException
import schemas
import models
import crud
from sqlalchemy.orm import Session
from database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/author/", response_model=list[schemas.AuthorRead])
def read_authors(skip: int = 0,
                 limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.AuthorRead)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.get("/books/", response_model=list[schemas.BookRead])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/books/author/{author_id}", response_model=list[schemas.BookRead])
def read_books_by_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_books_by_author(db=db, author_id=author_id)


@app.post("/authors/{author_id}/books/", response_model=schemas.BookRead)
def create_book_for_author(author_id: int,
                           book: schemas.BookCreate,
                           db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book, author_id=author_id)
