"""FastAPI router for authors and books."""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import authors_crud, books_crud
from src.database.database import get_db
from src.database.models import DbAuthor, DbBook
from src.schemas.schemas import (
    AuthorCreateSchema,
    AuthorDetailSchema,
    AuthorReadSchema,
    BookCreateSchema,
    BookDetailSchema,
    BookReadSchema,
)

router = APIRouter()


@router.get("/authors/", response_model=Page[AuthorReadSchema])
async def get_authors(
    params: Params = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Get paginated list of authors."""
    query = select(DbAuthor).order_by(DbAuthor.id)
    return await paginate(db, query, params)


@router.get("/authors/{author_id}", response_model=AuthorDetailSchema)
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)):
    """Get author by id."""
    author = await authors_crud.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return AuthorDetailSchema.model_validate(author)


@router.post("/authors/", response_model=AuthorReadSchema)
async def create_author(
    author: AuthorCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    """Create a new author."""
    db_author = await authors_crud.create_author(db, author)
    return AuthorReadSchema.model_validate(db_author)


@router.get("/books/", response_model=Page[BookReadSchema])
async def get_books(
    params: Params = Depends(),
    db: AsyncSession = Depends(get_db),
    author_id: int | None = Query(
        None, description="Filter books by author ID"
    ),
):
    """Get paginated list of books, optionally filtered by author_id."""
    query = select(DbBook).order_by(DbBook.id)
    if author_id:
        query = query.where(DbBook.author_id == author_id)
    return await paginate(db, query, params)


@router.get("/books/{book_id}", response_model=BookDetailSchema)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """Get book by id."""
    book = await books_crud.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookDetailSchema.model_validate(book)


@router.post("/books/", response_model=BookReadSchema)
async def create_book(
    book: BookCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    """Create a new book."""
    try:
        db_book = await books_crud.create_book(db, book)
        return BookReadSchema.model_validate(db_book)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
