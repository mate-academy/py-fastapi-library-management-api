"""CRUD operations for books."""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.crud import authors_crud
from src.database.models import DbBook
from src.schemas.schemas import BookCreateSchema


async def get_all_books(db: AsyncSession, author_id: int | None = None):
    """Get all books, optionally filtered by author_id."""
    query = select(DbBook)
    if author_id:
        query = query.where(DbBook.author_id == author_id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_book_by_id(db: AsyncSession, book_id: int) -> None | DbBook:
    """Get book by id with author."""
    query = (
        select(DbBook)
        .options(selectinload(DbBook.author))
        .where(DbBook.id == book_id)
    )
    result = await db.execute(query)
    return result.scalars().first()


async def create_book(db: AsyncSession, book: BookCreateSchema):
    """Create a new book, checking for author existence and unique title."""
    author = await authors_crud.get_author_by_id(db, book.author_id)
    if not author:
        raise ValueError("Author does not exist")

    db_book = DbBook(**book.model_dump())
    db.add(db_book)
    try:
        await db.commit()
        await db.refresh(db_book)
        return db_book
    except IntegrityError:
        await db.rollback()
        raise ValueError("Book with this title already exists")
