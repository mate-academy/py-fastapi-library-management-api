from typing import Annotated
from fastapi import APIRouter, Query, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database import DatabaseDependency
from src.models import Author, Book
from src.schemas import (
    AuthorCreate,
    AuthorDetail,
    AuthorList,
    BookCreate,
    BookDetail,
    BookList,
)

library_router = APIRouter()


@library_router.get("/books", response_model=list[BookList], tags=["Book",])
async def get_books(
    db: DatabaseDependency,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0, le=100),
):
    query = select(Book).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@library_router.post("/book", response_model=BookCreate, tags=["Book",])
async def create_book(db: DatabaseDependency, book_create: BookCreate):
    book = Book(
        title=book_create.title,
        author_id=book_create.author_id,
        summary=book_create.summary,
    )
    try:
        db.add(book)
        await db.commit()
        await db.refresh(book)
    except HTTPException:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Happened a problem with creating a new book"
        )
    return book

limit = Annotated[int, Query(0, ge=0)]
@library_router.get("/authors", response_model=list[AuthorList], tags=["Author",])
async def get_authors(
    db: DatabaseDependency,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0, le=100),
):
    query = select(Author).options(joinedload(Author.books)).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.unique().scalars().all()


@library_router.post("/author", response_model=AuthorCreate, tags=["Author",])
async def create_author(
    db: DatabaseDependency,
    author_create: AuthorCreate,
):
    author = Author(
        name=author_create.name, bio=author_create.bio, books=author_create.books
    )
    try:
        db.add(author)
        await db.commit()
        await db.refresh(author)
    except HTTPException:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Happened a problem with creating a new author"
        )
    return author


@library_router.get("/book/{id}", response_model=BookDetail, tags=["Book",])
async def get_book_detail(db: DatabaseDependency, id: int):
    query = select(Book).where(Book.id == id)
    result = await db.execute(query)
    book = result.scalars().first()
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id={id} not found",
        )
    return book


@library_router.get("/author/{id}", response_model=AuthorDetail, tags=["Author",])
async def get_author_detail(db: DatabaseDependency, id: int):
    query = select(Author).where(Author.id == id)
    result = await db.execute(query)
    author = result.scalars().first()
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id={id} not found",
        )
    return author
