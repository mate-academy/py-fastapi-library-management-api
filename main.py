from typing import Annotated
from fastapi import FastAPI, Depends, Response, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import SessionLocal
from app.utils import get_author_or_404, get_book_or_404

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    name: Annotated[str | None, Query(max_length=30)] = None,
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db),
):
    return crud.get_author_list(name=name, db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author_by_id(author_id: int, db: Session = Depends(get_db)):
    db_author = get_author_or_404(author_id=author_id, db=db)
    return db_author


@app.post("/create_author/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.put("/authors/{author_id}/", response_model=schemas.Author)
def update_author(
    author: schemas.AuthorUpdate, author_id: int, db: Session = Depends(get_db)
):
    db_author = crud.update_author(author=author, author_id=author_id, db=db)
    return db_author


@app.patch("/authors/{author_id}/", response_model=schemas.Author)
def partial_update_author(
    author: schemas.AuthorUpdate, author_id: int, db: Session = Depends(get_db)
):
    db_author = crud.update_author(author=author, author_id=author_id, db=db)
    return db_author


@app.delete("/authors/{author_id}/")
def destroy_author(author_id: int, db: Session = Depends(get_db)):
    crud.delete_author(db=db, author_id=author_id)
    return Response(status_code=204)


@app.get("/authors/{author_id}/books", response_model=list[schemas.Book])
def read_books_by_author_id(author_id: int, db: Session = Depends(get_db)):
    get_author_or_404(author_id=author_id, db=db)
    return crud.get_book_list_by_author_id(author_id=author_id, db=db)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    sort_parameter: str = None,
    sort_asc: bool = True,
    title: Annotated[str | None, Query(max_length=60)] = None,
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db),
):
    return crud.get_book_list(
        title=title,
        db=db,
        skip=skip,
        limit=limit,
        sort_parameter=sort_parameter,
        sort_asc=sort_asc,
    )


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_book_by_id(book_id: int, db: Session = Depends(get_db)):
    db_book = get_book_or_404(db=db, book_id=book_id)
    return db_book


@app.post("/authors/{author_id}/create_book/", response_model=schemas.Book)
def create_book(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book, author_id=author_id)


@app.put("/books/{book_id}/", response_model=schemas.Book)
def update_book(
    book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)
):
    db_book = crud.update_book(book_id=book_id, book=book, db=db)
    return db_book


@app.patch("/books/{book_id}/", response_model=schemas.Book)
def partial_update_book(
    book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)
):
    db_book = crud.update_book(book_id=book_id, book=book, db=db)
    return db_book


@app.delete("/books/{book_id}/")
def destroy_book(book_id: int, db: Session = Depends(get_db)):
    crud.delete_book(db=db, book_id=book_id)
    return Response(status_code=204)
