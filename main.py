from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import Base, SessionLocal, engine
import crud
import schemas
import models

# Створення таблиць у БД автоматично при запуску
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API", version="1.0.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):

    stmt = select(models.Author).where(models.Author.name == author.name)
    existing_author = db.scalars(stmt).first()
    if existing_author:
        raise HTTPException(status_code=400, detail="Author with this name already exists")
    return crud.create_author(db=db, author=author)

@app.get("/authors/", response_model=list[schemas.AuthorResponse])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)

@app.get("/authors/{author_id}", response_model=schemas.AuthorResponse)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/{author_id}/books/", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    author = crud.get_author(db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, book=book, author_id=author_id)

@app.get("/books/", response_model=list[schemas.BookResponse])
def read_books(
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
    db: Session = Depends(get_db)
):
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
