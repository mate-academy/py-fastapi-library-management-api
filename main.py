from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database import schemas, crud
from database.engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def root() -> dict:
    return {'message': 'Hello World'}


@app.get('/authors/', response_model=List[schemas.Author])
def get_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
) -> List[schemas.Author]:
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get('/authors/{author_id}', response_model=schemas.Author)
def get_author(
        author_id: int,
        db: Session = Depends(get_db)
) -> schemas.Author:
    author = crud.get_author(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(
            status_code=404,
            detail='Author not found'
        )
    return author


@app.post('/authors/', response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author(db, author_id=author.id)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail='Author already exists'
        )
    return crud.create_author(db=db, author=author)


@app.get('/books/', response_model=List[schemas.Book])
def get_books(
    db: Session = Depends(get_db),
    author_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10
) -> List[schemas.Book]:
    return crud.get_all_books(
        db=db, author_id=author_id, skip=skip, limit=limit
    )


@app.post('/books/', response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.Book:
    author = crud.get_author(db=db, author_id=book.author_id)

    if author is None:
        raise HTTPException(
            status_code=400,
            detail='Author does not exist'
        )
    return crud.create_book(db=db, book=book)
