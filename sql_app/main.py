from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud
from sql_app import schemas
from sql_app.database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/authors/", response_model=list[schemas.AuthorRetrieve])
def read_all_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.AuthorRetrieve)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db, author_name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail=f"Author with name {db_author.name} already registered")
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorRetrieve)
def read_author_by_id(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail=f"Author with id {author_id} not found")
    return db_author


@app.get("/books/", response_model=list[schemas.BookRetrieve])
def read_all_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_books(db, skip=skip, limit=limit)


@app.get("/books/{book_id}/", response_model=schemas.BookRetrieve)
def read_book_by_id(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail=f"book with id {book_id} not found")
    return db_book


@app.get("/books/authors/{author_id}/", response_model=list[schemas.BookRetrieve])
def read_books_by_author(author_id: int, db: Session = Depends(get_db)):
    return crud.filter_books_by_author(db=db, author_id=author_id)


@app.post("/books/create/", response_model=schemas.BookRetrieve)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_title(db, title=book.title)
    if db_book:
        raise HTTPException(
            status_code=400,
            detail="This title exists"
        )
    return crud.create_book(db=db, book=book)
