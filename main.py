from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schema
from database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/author/", response_model=list[schema.AuthorRead])
async def authors_get_list(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return crud.get_list_authors(db, skip, limit)


@app.get("/author/{author_pk}", response_model=schema.AuthorRead)
async def author_get_detail(author_pk: int, db: Session = Depends(get_db)):
    author = crud.get_detail_author(db, author_pk)
    if author is None:
        raise HTTPException(status_code=404, detail="User not found")
    return author


@app.post("/author/", response_model=schema.AuthorRead)
async def author_post_list(author: schema.AuthorBase, db: Session = Depends(get_db)):
    return crud.post_list_author(db, author)


@app.get("/book/", response_model=list[schema.BookRead])
async def book_get_list(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return crud.get_list_books(db, skip, limit)


@app.get(
    "/author/{author_pk}/books/",
    response_model=list[schema.BookRead]
)
async def book_get_detail(author_pk: int, db: Session = Depends(get_db)):
    book = crud.get_detail_book(db, author_pk)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/book/", response_model=schema.BookRead)
async def book_post_list(book: schema.BookCreate, db: Session = Depends(get_db)):
    return crud.post_list_book(db, book)
