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


@app.get("/author/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    authors = crud.get_all_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/author/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_author(db=db, author_id=author_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_book


@app.post("/author/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such name for author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.patch("/author/{author_id}/", response_model=schemas.Author)
def update_author(author_id: int, author: schemas.Author, db: Session = Depends(get_db)):
    db_author = crud.update_author(db, author_id=author_id, author=author)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.delete("/author/{author_id}/", response_model=schemas.Author)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.delete_author(db, author_id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.get("/book/", response_model=list[schemas.Book])
def read_book(
        db: Session = Depends(get_db),
        author: str | None = None,
        skip: int = 0,
        limit: int = 5,
):
    return crud.get_book_list(db=db, author=author, skip=skip, limit=limit)


@app.get("/book/{book_id}/", response_model=schemas.Book)
def read_single_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="book not found")

    return db_book


@app.post("/book/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.patch("/book/{book_id}/", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.Book, db: Session = Depends(get_db)):
    db_book = crud.update_book(db, book_id=book_id, book=book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.delete("/book/{book_id}/", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.delete_book(db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book
