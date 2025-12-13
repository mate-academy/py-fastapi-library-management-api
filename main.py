from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastApi(title="Library Management API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author, status_code=201)
def create_author_endpoint(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    existing_author = db.query(models.Author).filter(models.Author.name == author.name).first()
    if existing_author:
        raise HTTPException(status_code=400, detail="Author with this name already exists")
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author_endpoint(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/books/", response_model=schemas.Book, status_code=201)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id=book.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_author_book(db=db, book=book)


@app.get("/books/", response_model=List[schemas.Book])
def read_books_endpoint(
        skip: int = 0,
        limit: int = 10,
        author_id: Optional[int] = Query(None, description="Filter books by author ID"),
        db: Session = Depends(get_db)
):
    books = crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
    return books






