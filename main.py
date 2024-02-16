from fastapi import FastAPI, Depends, HTTPException
import schemas
import crud
from db.engine import SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors_list(db: Session = Depends(get_db)):
    return crud.get_all_authors(db)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author_by_id(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author_model = crud.get_author_by_name(db=db, name=author.name)

    if db_author_model:
        raise HTTPException(status_code=400, detail="This name of author already exist")

    return crud.create_author(db=db, author=author)


@app.get("/books/")
def read_all_authors(
        author_id: int | None = None,
        db: Session = Depends(get_db)
):
    db_book = crud.get_books_list(db=db, author_id=author_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_all_authors(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.post("/books/")
def create_author(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)
