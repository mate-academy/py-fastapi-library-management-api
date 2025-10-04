from typing import List, Generator, Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from library_book import models, schemas, crud
from library_book.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def get_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    author = crud.get_author(db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, author_id=author_id, book=book)


@app.get("/books/", response_model=List[schemas.Book])
def get_books(
    skip: int = 0,
    limit: int = 10,
    author_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
