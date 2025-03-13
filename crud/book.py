from typing import Optional

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas


async def get_book_list(
    db: AsyncSession,
    author_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 2
):
    query = select(models.Book)

    if author_id is not None:
        query = query.where(models.Book.author_id == author_id)

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    books = result.scalars().all()

    return books


async def get_book(db: AsyncSession, book_id: int):
    query = select(models.Book).where(models.Book.id == book_id)

    result = await db.execute(query)

    book = result.scalar_one_or_none()

    return book


async def add_book(db: AsyncSession, book: schemas.BookCreate):
    query = insert(models.Book).values(
        title=book.title,
        summary=book.summary,
        author_id=book.author_id,
    )

    result = await db.execute(query)

    await db.commit()

    response = {**book.model_dump(), "id": result.lastrowid}

    return response
