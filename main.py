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
def root():
    return {"message": "Welcome to Library API"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return crud.get_author_list(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db=db, author_id=author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(
    author_id: int, author: schemas.AuthorCreate, db: Session = Depends(get_db)
):
    updated_author = (
        crud.update_author(db=db, author_id=author_id, author=author)
    )

    if not updated_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return updated_author


@app.delete("/authors/{author_id}", response_model=dict)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    deleted_successfully = crud.delete_author(db=db, author_id=author_id)
    if deleted_successfully:
        return {"message": "Author deleted successfully"}

    raise HTTPException(status_code=404, detail="Author not found")


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return crud.get_book_list(
        db=db, author_id=author_id, skip=skip, limit=limit
    )


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db=db, book_id=book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(
    book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    updated_book = crud.update_book(db=db, book_id=book_id, book=book)

    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return updated_book


@app.delete("/books/{book_id}", response_model=dict)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted_successfully = crud.delete_book(db=db, book_id=book_id)
    if deleted_successfully:
        return {"message": "Book deleted successfully"}

    raise HTTPException(status_code=404, detail="Book not found")
