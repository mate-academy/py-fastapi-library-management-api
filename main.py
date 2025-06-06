from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import SessionLocal

import schemas
import crud


app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close() 



@app.get("/")
def root():
    return {"message": "LIBRARY"} 


@app.post("/authors/", response_model=schemas.Author)
def create_new_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with such name alredy exists."
        )

    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def list_all_authors(
    skip: int = Query(0, description="Number of authors to skip"),
    limit: int = Query(10, description="Max authors to retrieve"),
    db: Session = Depends(get_db)
):
    
    return crud.get_list_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def single_author_by_id(
    author_id: int,
    db: Session = Depends(get_db)
):
    author = crud.get_author_by_id(db=db, author_id=author_id)
    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author with this ID not found."
        )
    
    return author


@app.post("/books/", response_model=schemas.Book)
def create_new_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):

    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def list_all_books(
    author_id: int | None = None,
    skip: int = Query(0, description="Number of books to skip"),
    limit: int = Query(10, description="Max books to retrieve"),
    db: Session = Depends(get_db)
): 
    
    return crud.get_list_books(db=db, author_id=author_id, skip=skip, limit=limit)


@app.get("/books/{book_id}/", response_model=schemas.Book)
def single_book_by_id(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = crud.get_book_by_id(db=db, book_id=book_id)
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book with this ID not found."
        )
    
    return book
