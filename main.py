import crud
import schemas
from database import Base, engine, SessionLocal
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException


app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def get_bd(db: Session = Depends(get_db)):
    return "Database connected"

@app.post("/authors/", response_model=schemas.AuthorResponse)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db, author)

@app.get("/authors/", response_model=list[schemas.AuthorResponse])
def get_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return crud.get_all_authors(db, skip, limit)

@app.get("/authors/{author_id}", response_model=schemas.AuthorResponse)
def get_author_by_id(
        author_id: int,
        db: Session = Depends(get_db)
):
    author_db = crud.get_author_by_id(db, author_id)
    if author_db is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author_db


@app.get("/books/", response_model=list[schemas.BookResponse])
def get_books(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return crud.get_all_books(db, skip, limit)

@app.post("/authors/{author_id}/books/", response_model=schemas.BookResponse)
def create_book(
        author_id: int,
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    if not crud.get_author_by_id(db, author_id):
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db, book, author_id)

@app.get("/books/by-author/", response_model=list[schemas.BookResponse])
def get_books_by_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    return crud.get_books_by_author_id(db, author_id)
