from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
from db.database import SessionLocal, engine, Base
from schemas import AuthorCreate, Book, BookCreate, Author

app = FastAPI(title="Library Management API")

Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/author", response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(author=author, db=db)


@app.get("/authors", response_model=list[Author])
def get_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/author/{author_id}", response_model=Author)
def get_authors_by_id(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db=db, author_id=author_id)


@app.post("/book", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(book=book, db=db)


@app.get("/books", response_model=list[Book])
def get_books(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
        author_id: int = None
):
    return crud.get_books(db=db, skip=skip, limit=limit, author_id=author_id)
