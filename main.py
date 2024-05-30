from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import schemas
from database import SessionLocal
from models import Author, Book

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get('/')
def root() -> dict[str, str]:
    return {'message': 'All working at this endpoint'}


@app.get('/author/', response_model=schemas.Author)
def get_all_authors(db: Session = Depends(get_db),
                    skip: int | None = None,
                    limit: int | None = None) -> list[Author]:
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.post('/author/', response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> schemas.Author:
    db_authors = crud.get_author_by_name(db=db, author_name=author.name)

    if db_authors:
        raise HTTPException(status_code=400,
                            detail='This Author already exist')
    return crud.create_author(db=db, author=author)


@app.get('/author/{author_id}', response_model=schemas.Author)
def get_author_by_id(author_id: int,
                     db: Session = Depends(get_db)) -> schemas.Author:
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail='Author not found')

    return db_author


@app.get('/book/', response_model=schemas.Book)
def get_all_books(db: Session = Depends(get_db),
                  skip: int | None = None,
                  limit: int | None = None,
                  author_id: int = None) -> list[Book]:
    return crud.get_all_books(db=db, skip=skip,
                              limit=limit, author_id=author_id)


@app.post('/book/', response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.Book:
    db_books = crud.get_book_by_title(db=db, book_title=book.title)

    if db_books:
        raise HTTPException(status_code=400,
                            detail='This book already exist')
    return crud.create_book(db=db, book=book)
