from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import SessionLocal
import models
import schemas
import crud

app = FastAPI(title="Author & Book Management API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post(
    "/authors/", 
    response_model=schemas.AuthorList, 
    status_code=status.HTTP_201_CREATED
)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = db.query(models.DBAuthor).filter(models.DBAuthor.name == author.name).first()
    if db_author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Author with this name already exists"
        )
    return crud.create_author(db=db, author=author)

@app.get("/authors/", response_model=List[schemas.AuthorList])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    from sqlalchemy.orm import joinedload
    authors = (
        db.query(models.DBAuthor)
        .options(joinedload(models.DBAuthor.books))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return authors

@app.get("/authors/{author_id}", response_model=schemas.AuthorList)
def read_author(author_id: int, db: Session = Depends(get_db)):
    from sqlalchemy.orm import joinedload
    db_author = (
        db.query(models.DBAuthor)
        .options(joinedload(models.DBAuthor.books))
        .filter(models.DBAuthor.id == author_id)
        .first()
    )
    if db_author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Author not found"
        )
    return db_author

@app.post(
    "/authors/{author_id}/books/", 
    response_model=schemas.BookList, 
    status_code=status.HTTP_201_CREATED
)
def create_book_for_author(
    author_id: int, 
    book: schemas.BookCreate, 
    db: Session = Depends(get_db)
):
    db_author = db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()
    if db_author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Author not found"
        )
    return crud.create_book_for_author(db=db, book=book, author_id=author_id)

@app.get("/books/", response_model=List[schemas.BookList])
def read_books(
    skip: int = 0, 
    limit: int = 10, 
    author_id: Optional[int] = None, 
    db: Session = Depends(get_db)
):
    query = db.query(models.DBBook)

    if author_id is not None:
        query = query.filter(models.DBBook.author_id == author_id)
        
    books = query.offset(skip).limit(limit).all()
    return books
