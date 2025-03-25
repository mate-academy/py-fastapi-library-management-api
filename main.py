

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from crud import crud
from db.database import SessionLocal
from schema import schemas

app = FastAPI()


def get_db() -> Session:
    with SessionLocal() as db:
        yield db


@app.get("/author/", response_model=list[schemas.Author])
def read_author(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_author_list(db)[skip: skip + limit]


@app.get("/author/{author_id}", response_model=schemas.Author)
def read_author_detail(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_autor_detail(author_id=author_id, db=db)
    if author is None:
        raise HTTPException(
            status_code=404,
            detail=f"Author with id: {author_id} not exist"
        )

    return author


@app.post("/author/", response_model=schemas.AuthorCreate)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/book/", response_model=list[schemas.Book])
def read_book(
        author: int | None = None,
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return crud.get_book_list(db=db, author=author)[skip: skip + limit]


@app.get("/book/{book_id}", response_model=schemas.Book)
def read_book_detail(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book_detail(book_id=book_id, db=db)
    if book is None:
        raise HTTPException(
            status_code=404,
            detail=f"Book with id: {book_id} not exist"
        )

    return book


@app.post("/book/", response_model=schemas.BookCreate)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
