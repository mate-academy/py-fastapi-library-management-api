from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from crud import create_author, add_book_to_db, get_list_author_from_db, get_list_books_from_db, \
    get_book_by_author_id_from_db, get_author_by_id_from_db
from database import SessionLocal, engine
from models import Author, Book
from schemas import AuthorCreateResponseSchema, AuthorCreateSchema, AuthorListSchema, \
    BookCreateResponseSchema, BookCreateSchema

from models import Base


Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


"""AUTHOR ENDPOINTS"""
@app.post("/author/create/", response_model=AuthorCreateResponseSchema)
def author_create(data: AuthorCreateSchema, db: Session = Depends(get_db)):

    request = db.execute(select(Author).where(Author.name == data.name))
    author = request.scalars().first()
    if author:
        raise HTTPException(status_code=400, detail=f"Author with such name: {author.name} already exist!")

    return create_author(data=data, db=db)


@app.get("/author/list/", response_model=List[AuthorListSchema])
def get_authors(db: Session = Depends(get_db), skip: int = 0 , limit: int = 10):
    return get_list_author_from_db(db=db, skip=skip, limit=limit)


@app.get("/author/{author_id}/", response_model=AuthorListSchema)
def retrieve_author_by_id(author_id: int, db: Session = Depends(get_db)):
    request = db.execute(select(Author).where(Author.id == author_id))
    author = request.scalars().first()
    if not author:
        raise HTTPException(status_code=400, detail=f"Author with the given ID: {author_id} not found!")

    return author



"""BOOK ENDPOINTS"""

@app.post("/book/create/", response_model=BookCreateResponseSchema)
def create_book(data: BookCreateSchema, db: Session = Depends(get_db)):
    request = db.execute(select(Author).where(Author.id == data.author_id))
    author = request.scalars().first()

    if not author:
        raise HTTPException(status_code=404, detail=f"Author with the given ID: {data.author_id} does not exist")

    return add_book_to_db(data=data, db=db)


@app.get("/book/list/", response_model=List[BookCreateResponseSchema])
def get_books(db: Session = Depends(get_db), skip: int = 0 , limit: int = 10):
    return get_list_books_from_db(db=db, skip=skip, limit=limit)


@app.get("/book/{author_id}/", response_model=List[BookCreateResponseSchema])
def get_authors_book(author_id: int, db: Session = Depends(get_db)):

    return get_book_by_author_id_from_db(author_id=author_id, db=db)
