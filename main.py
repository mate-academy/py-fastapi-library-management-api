from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import SessionLocal
import crud
import schemas

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/author/", response_model=list[schemas.Author])
def get_author(
    skip: int = Query(0),
    limit: int = Query(10),
    db: Session = Depends(get_db)
):
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.post("/author/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author already exists",
        )

    return crud.create_author(db=db, author=author)


@app.get("/book/", response_model=list[schemas.Book])
def get_book(
    skip: int = Query(0),
    limit: int = Query(10),
    db: Session = Depends(get_db)
):
    return crud.get_all_books(db, skip=skip, limit=limit)


@app.get("/book/{book_id}", response_model=schemas.Book)
# it's work, it's ok
def read_single_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )
    return db_book


@app.post("/book/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
