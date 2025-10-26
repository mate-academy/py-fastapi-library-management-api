from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Author, Book
from schemas import AuthorCreate, AuthorUpdate, BookCreate, BookUpdate


async def get_books_list(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    author_id: Optional[int] = None
) -> List[Book]:
    stmt = select(Book)
    if author_id:
        stmt = stmt.where(Book.author_id == author_id)
    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_authors_list(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10
) -> List[Author]:
    stmt = select(Author).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_author_by_id(db: AsyncSession, pk: int) -> Author:
    author = await db.get(Author, pk)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


async def get_book_by_id(db: AsyncSession, pk: int) -> Book:
    book = await db.get(Book, pk)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


async def create_book(
    db: AsyncSession,
    book_data: BookCreate
) -> Book:
    new_book = Book(
        title=book_data.title,
        summary=book_data.summary,
        publication_date=book_data.publication_date,
        author_id=book_data.author_id
    )

    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

async def create_author(
    db: AsyncSession,
    author_data: AuthorCreate
) -> Author:
    existing_author = await db.execute(
        select(Author).where(Author.name == author_data.name)
    )
    if existing_author.scalars().first():
        raise HTTPException(status_code=400, detail="Author with following name already exists")

    new_author = Author(
        name=author_data.name,
        bio=author_data.bio,
        books=author_data.books
    )

    db.add(new_author)
    await db.commit()
    await db.refresh(new_author)
    return new_author


async def update_author(
    db: AsyncSession,
    pk: int,
    author_update_data: AuthorUpdate
) -> Author:
    author_to_update = await get_author_by_id(db=db, pk=pk)
    author_to_update.name = author_update_data.name
    author_to_update.bio = author_update_data.bio
    await db.commit()
    await db.refresh(author_to_update)
    return author_to_update


async def update_book(
    db: AsyncSession,
    pk: int,
    book_update_data: BookUpdate
) -> Book:
    book_to_update = await get_book_by_id(db=db, pk=pk)
    book_to_update.title = book_update_data.title
    book_to_update.summary = book_update_data.summary
    book_to_update.publication_date = book_update_data.publication_date
    book_to_update.author_id = book_update_data.author_id
    await db.commit()
    await db.refresh(book_to_update)
    return book_to_update


async def delete_author(db: AsyncSession, pk: int) -> dict:
    author = await get_author_by_id(db=db, pk=pk)
    await db.delete(author)
    await db.commit()
    return {"message": "Author deleted successfully"}


async def delete_book(db: AsyncSession, pk: int) -> dict:
    book = await get_book_by_id(db=db, pk=pk)
    await db.delete(book)
    await db.commit()
    return {"message": "Book deleted successfully"}
