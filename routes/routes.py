from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm.session import Session

from database.database import get_db
from routes import crud
from schemas import schemas

router = APIRouter()


@router.post("/authors/", response_model=schemas.AuthorCreateResponse, status_code=201)
def create_author(
    data: schemas.AuthorCreateRequest, db: Session = Depends(get_db)
) -> schemas.AuthorCreateResponse:
    author = crud.create_new_author(db=db, name=data.name, bio=data.bio)

    return schemas.AuthorCreateResponse.model_validate(author)


@router.get("/authors/", response_model=schemas.AuthorListResponse)
def get_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_db),
) -> schemas.AuthorListResponse:
    authors = crud.get_authors_paginated(db, skip, limit)
    return schemas.AuthorListResponse(authors=authors)


@router.get("/authors/{author_id}/", response_model=schemas.AuthorCreateResponse)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_single_author(db, author_id)
    return schemas.AuthorCreateResponse.model_validate(author)


@router.post("/books/", response_model=schemas.BookCreateResponse, status_code=201)
def create_book(
    data: schemas.BookCreateRequest, db: Session = Depends(get_db)
) -> schemas.BookCreateResponse:
    book = crud.create_new_book_for_specific_author(
        db=db,
        author_id=data.author_id,
        title=data.title,
        summary=data.summary,
        publication_date=data.publication_date,
    )
    return schemas.BookCreateResponse.model_validate(book)


@router.get("/books/", response_model=schemas.BookListResponse)
def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_db),
) -> schemas.AuthorListResponse:
    books = crud.get_books_paginated(db, skip, limit)
    return schemas.BookListResponse(books=books)


@router.get("/authors/{author_id}/books/", response_model=schemas.BookListResponse)
def get_books_by_author(
    author_id: int, db: Session = Depends(get_db)
) -> schemas.BookListResponse:
    books = crud.get_books_by_author_id(db, author_id)
    return schemas.BookListResponse(books=books)
