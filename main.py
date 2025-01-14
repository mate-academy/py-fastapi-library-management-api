from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import (
    get_all_authors,
    get_author_by_name,
    get_book_list,
    create_book as crud_create_book,
    get_author_by_id,
)
from schemas import Author, AuthorCreate, Book, BookCreate
from db.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[Author])
def read_authors(db: Session = Depends(get_db)):
    return get_all_authors(db=db)


@app.get("/authors/{author_id}/", response_model=Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = get_author_by_id(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/", response_model=Author)
def create_author(
    author: AuthorCreate,
    db: Session = Depends(get_db),
):
    db_author = get_author_by_name(db=db, name=author.name)

    if db_author is None:
        raise HTTPException(
            status_code=400, detail="Such name for author already exists"
        )

    return create_author(db=db, author=author)


@app.get("/books/", response_model=list[Book])
def read_books(db: Session = Depends(get_db)):
    return get_book_list(
        db=db,
    )


@app.post("/books/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    author = get_author_by_id(db=db, author_id=book.author_id)

    if not author:
        raise HTTPException(status_code=400, detail="Author does not exist")

    return crud_create_book(db=db, book=book)
