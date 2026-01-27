from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from models import Author, Book
from schemas import AuthorCreateSchema, BookCreateSchema


async def get_all_authors(db: AsyncSession) -> List[Author]:
    result = await db.execute(select(Author).options())
    return result.scalars().all()


async def get_author_by_id(db: AsyncSession, author_id: int) -> Author | None:
    result = await db.execute(select(Author).where(Author.id == author_id))
    return result.scalar_one_or_none()


async def create_author(
    db: AsyncSession,
    author_in: AuthorCreateSchema
) -> Author:
    author = Author(
        name=author_in.name,
        bio=author_in.bio
    )
    db.add(author)
    await db.commit()
    await db.refresh(author)
    return author


async def get_all_books(db: AsyncSession) -> List[Book]:
    result = await db.execute(select(Book))
    return result.scalars().all()


async def get_book_by_id(db: AsyncSession, book_id: int) -> Book | None:
    result = await db.execute(select(Book).where(Book.id == book_id))
    return result.scalar_one_or_none()


async def create_book(db: AsyncSession, book_in: BookCreateSchema) -> Book:
    book = Book(
        title=book_in.title,
        summary=book_in.summary,
        publication_date=book_in.publication_date,
        author_id=book_in.author_id
    )
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book
