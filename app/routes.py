from sqlalchemy.orm import Session
from typing import List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app import crud
from app import serializers
from app.database import get_db
from app.config import settings
from app.models import (
    DBAuthor,
    DBBook
)

router = APIRouter()


@router.get("/authors/", response_model=List[serializers.Author])
def read_authors_list(
        db: Session = Depends(get_db),
        skip: int = settings.DEFAULT_SKIP_VALUE,
        limit: int = settings.DEFAULT_LIMIT_VALUE
) -> List[DBAuthor]:
    authors = crud.get_author_list(db, skip=skip, limit=limit)
    return authors


@router.get("/authors/{author_id}", response_model=serializers.Author)
def read_author_by_id(
        author_id: int,
        db: Session = Depends(get_db)
) -> DBAuthor:
    author = crud.get_author_by_id(db, author_id)

    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author with this id not exists"
        )
    return author


@router.post("/authors/", response_model=serializers.Author)
def create_author(
        author: serializers.AuthorCreate,
        db: Session = Depends(get_db)
) -> DBAuthor:
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exists"
        )

    return crud.create_author(db=db, author=author)


@router.get("/books/", response_model=List[serializers.Book])
def read_book_list(
        db: Session = Depends(get_db),
        skip: int = settings.DEFAULT_SKIP_VALUE,
        limit: int = settings.DEFAULT_LIMIT_VALUE
) -> List[DBBook]:
    return crud.get_books_list(db=db, skip=skip, limit=limit)


@router.get("/books/{author_id}/", response_model=List[serializers.Book])
def get_single_book(
        author_id: int,
        db: Session = Depends(get_db)
) -> DBBook:
    author = read_author_by_id(author_id=author_id, db=db)
    db_books = crud.get_books_by_author_id(author_id=author.id, db=db)

    if not db_books:
        raise HTTPException(
            status_code=404,
            detail="Books for that author not found"
        )

    return db_books


@router.post("/books/", response_model=serializers.Book)
def create_book(
        book: serializers.BookCreate,
        db: Session = Depends(get_db)
) -> DBBook:
    return crud.create_book(db=db, book=book)
