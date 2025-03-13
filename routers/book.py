from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from crud.book import get_book, get_book_list, add_book
from schemas import Book, BookCreate


router = APIRouter()


@router.get("/", response_model=List[Book])
async def read_books(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 2,
    author_id: Optional[int] = None
):
    books = await get_book_list(db, author_id, skip, limit)
    return books


@router.get("/{book_id}", response_model = Book)
async def read_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await get_book(db=db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=BookCreate)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    new_book = await add_book(db=db, book=book)
    return new_book
