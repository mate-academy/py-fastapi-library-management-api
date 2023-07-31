from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_authors(db)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author(db=db, author_id=author_id)


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(status_code=400, detail="Such author already exists")

    return crud.create_author(db=db, author=author)


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    return crud.create_author_book(db=db, author_id=author_id, book=book)


@app.delete("/authors/{author_id}/", response_model=schemas.Author)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.delete_author(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Such author does not exist")

    return db_author


@app.put("/authors/{author_id}/", response_model=schemas.Author)
def update_author(
    author_id: int, author_data: schemas.AuthorCreate, db: Session = Depends(get_db)
):
    db_author = crud.update_author(
        db=db, author_id=author_id, updated_data=author_data.model_dump()
    )

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    books = crud.get_books(skip=skip, limit=limit, db=db)

    return books


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    return crud.get_book(db=db, book_id=book_id)


@app.get("/books/by_title/{book_title}/", response_model=schemas.Book)
def read_book_by_title(book_title: str, db: Session = Depends(get_db)):
    return crud.get_book_by_title(db=db, title=book_title)


@app.get("/books/{author_id}", response_model=list[schemas.Book])
def read_books_by_author_id(
    author_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_books(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit,
    )


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    author = crud.get_author(db=db, author_id=book.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author does not exist.")

    db_book = crud.get_book_by_title(db=db, title=book.title)
    if db_book:
        raise HTTPException(
            status_code=409, detail="Book with this title already exists."
        )

    return crud.create_book(db=db, book=book)


@app.delete("/books/{book_id}/", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.delete_book(db=db, book_id=book_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="Such author does not exist")

    return db_book


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(
    book_id: int, book_data: schemas.BookCreate, db: Session = Depends(get_db)
):
    db_book = crud.update_book(
        db=db, book_id=book_id, updated_data=book_data.model_dump()
    )

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book
