from fastapi import APIRouter, Query, status, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import DatabaseDependency
from models import Author, Book
from schemas import (
    AuthorCreate,
    AuthorDetail,
    AuthorList,
    BookCreate,
    BookDetail,
    BookList,
    BookFilter
)

library_router = APIRouter()


@library_router.get("/books", response_model=list[BookList], tags=["Book",])
async def get_books(
    db: DatabaseDependency,
    author_filter: BookFilter = Depends(),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0, le=100),
):
    query = select(Book).offset(skip).limit(limit)
    if author_filter.author_id:
        query = query.where(Book.author_id == author_filter.author_id)
    result = await db.execute(query)
    return result.scalars().all()


@library_router.post("/book", response_model=BookCreate, tags=["Book",])
async def create_book(db: DatabaseDependency, book_create: BookCreate):
    book_data = book_create.model_dump(exclude_none=True)
    book = Book(**book_data)
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

@library_router.get("/authors", response_model=list[AuthorList], tags=["Author",])
async def get_authors(
    db: DatabaseDependency,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0, le=100),
):
    query = select(Author).options(selectinload(Author.books)).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.unique().scalars().all()


@library_router.post("/author", response_model=AuthorCreate, tags=["Author",])
async def create_author(
    db: DatabaseDependency,
    author_create: AuthorCreate,
):
    author_data = author_create.model_dump(exclude_none=True)
    author = Author(**author_data)
    try:
        db.add(author)
        await db.commit()
        await db.refresh(author, attribute_names=["books"])
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
    query = select(Author).where(Author.id == id).options(selectinload(Author.books)).where(Author.id == id)
    result = await db.execute(query)
    author = result.scalars().first()
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id={id} not found",
        )
    return author
