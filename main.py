from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"Hello": "World"}


@app.get("/books/", response_model=schemas.PaginatedBooks)
def read_books(
        author_id: int = None,
        title: str = None,
        sort_by: str = None,
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    books = crud.get_all_books(db=db, author_id=author_id, skip=skip, limit=limit, title=title, sort_by=sort_by)
    total = crud.get_book_count(db=db)
    return schemas.PaginatedBooks(total=total, items=books)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    if not crud.get_author(db=db, author_id=book.author_id):
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, book=book)


@app.patch("/books/{book_id}/", response_model=schemas.Book)
def update_book(book_id: int, db: Session = Depends(get_db), book: schemas.BookUpdate = None):
    db_book = crud.get_book(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_book = crud.update_book(db=db, db_book=db_book, book=book)
    return db_book


@app.delete("/books/{book_id}/")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    crud.delete_book(db_book=db_book, db=db)
    return {"message": "Book deleted"}


@app.get("/authors/", response_model=schemas.PaginatedAuthors)
def read_authors(name: str = None, sort_by: str = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = crud.get_all_authors(db=db, skip=skip, limit=limit, name=name, sort_by=sort_by)
    total = crud.get_author_count(db=db)
    return schemas.PaginatedAuthors(total=total, items=authors)


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)) -> schemas.Author:
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.patch("/authors/{author_id}/", response_model=schemas.Author)
def update_author(author_id: int, db: Session = Depends(get_db), author: schemas.AuthorUpdate = None):
    db_author = crud.get_author(db=db, author_id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    db_author = crud.update_author(db=db, db_author=db_author, author=author)
    return db_author


@app.delete("/authors/{author_id}/")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    crud.delete_author(db=db, db_author=db_author)
    return {"message": "Author deleted"}
