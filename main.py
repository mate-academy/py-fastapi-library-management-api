from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def list_authors(db: Session = Depends(get_db)):
    return crud.get_author_list(db=db)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def detail_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    return crud.get_author_by_id(db=db, author_id=author_id)


@app.put("/authors/{author_id}/", response_model=schemas.Author)
def update_author(
        author_id: int,
        author: schemas.AuthorUpdate,
        db: Session = Depends(get_db)
):
    return crud.update_author(db=db, author_id=author_id, author=author)


@app.delete("/authors/{author_id}/", response_model=schemas.DeleteResponse)
def delete_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    crud.delete_author(db=db, author_id=author_id)
    return {"message": "Author successfully deleted", "deleted_id": author_id}


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def list_books(
        author_id: int | None = None,
        db: Session = Depends(get_db)
):
    return crud.get_book_list(db=db, author_id=author_id)


@app.get("/books/{book_id}/", response_model=schemas.Book)
def detail_book(
        book_id: int,
        db: Session = Depends(get_db)
):
    return crud.get_book_by_id(db=db, book_id=book_id)


@app.put("/books/{book_id}/", response_model=schemas.Book)
def update_book(
        book_id: int,
        book: schemas.BookUpdate,
        db: Session = Depends(get_db)
):
    return crud.update_book(db=db, book_id=book_id, book=book)


@app.delete("/books/{book_id}/", response_model=schemas.DeleteResponse)
def delete_book(
        book_id: int,
        db: Session = Depends(get_db)
):
    crud.delete_book(db=db, book_id=book_id)
    return {"message": "Book successfully deleted", "deleted_id": book_id}
