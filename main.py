from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int | None = 0,
        limit: int | None = 10,
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
):
    try:
        return crud.create_author(db=db, author=author)
    except crud.AuthorNameAlreadyExistsError:
        raise HTTPException(
            status_code=400,
            detail="Such name for Author already exists",
        )


@app.put("/authors/{author_id}/", response_model=schemas.Author)
def update_author(
    author_id: int,
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud.update_author(db=db, author_id=author_id, author=author)
    except crud.AuthorNotFoundError:
        raise HTTPException(status_code=404, detail="Author not found")
    except crud.AuthorNameAlreadyExistsError:
        raise HTTPException(
            status_code=400,
            detail="Such name for Author already exists",
        )


@app.delete("/authors/{author_id}/", status_code=204)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_author(db=db, author_id=author_id)
    except crud.AuthorNotFoundError:
        raise HTTPException(status_code=404, detail="Author not found")


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        db: Session = Depends(get_db),
        author_id: int | None = None,
        skip: int | None = 0,
        limit: int | None = 10,
):
    return crud.get_all_books(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit,
    )


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
):
    db_author = crud.get_author(db=db, author_id=book.author_id)
    if db_author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )
    return crud.create_book(db=db, book=book)


@app.put("/books/{book_id}/", response_model=schemas.Book)
def update_book(
    book_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud.update_book(
            db=db,
            book_id=book_id,
            book=book,
        )
    except crud.BookNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )


@app.delete("/books/{book_id}/", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_book(db=db, book_id=book_id)
    except crud.BookNotFoundError:
        raise HTTPException(status_code=404, detail="Book not found")
