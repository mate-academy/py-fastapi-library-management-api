import crud
import schemas
from database import SessionLocal
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_pagination import paginate, Page, add_pagination

from crud import get_all_authors

app = FastAPI()

add_pagination(app)


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/authors/", response_model=Page[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    return paginate(get_all_authors(db))


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def retrieve_author_by_id(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db, author_id)

    if not db_author:
        raise HTTPException(
            status_code=404,
            detail="Author nor found"
        )
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such name for Author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=Page[schemas.Book])
def read_books(db: Session = Depends(get_db)):
    return paginate(crud.get_all_books(db))


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    db_book = crud.get_book_by_title(db=db, title=book.title)
    if db_book:
        raise HTTPException(
            status_code=400,
            detail="Such title for Book already exists"
        )

    return crud.create_book(db=db, book=book)


@app.get("/books/{author_id}", response_model=list[schemas.Book])
def retrieve_book(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_book_by_author_id(db=db, pk=author_id)

    if not db_author:
        raise HTTPException(
            status_code=404,
            detail="Book with such author not found"
        )

    return db_author
