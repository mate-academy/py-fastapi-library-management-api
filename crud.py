from sqlalchemy.future import select
from sqlalchemy.orm import AsyncSession

import models
import schemas


async def get_authors(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
) -> list[models.Author]:
    query = select(models.Author).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def create_author(
        db: AsyncSession,
        author: schemas.AuthorCreate
) -> models.Author:
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    await db.commit()
    await db.refresh(db_author)

    return db_author


async def get_author_by_name(db: AsyncSession, name: str) -> models.Author | None:
    query = select(models.Author).filter(models.Author.name == name)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_author_by_id(
    db: AsyncSession,
    author_id: int
) -> models.Author | None:
    query = select(models.Author).filter(models.Author.id == author_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_books(
    db: AsyncSession,
    author_id: int = None,
    skip: int = 0,
    limit: int = 100
) -> list[models.Book]:
    query = select(models.Book).offset(skip).limit(limit)

    if author_id:
        query = query.filter(models.Book.author_id == author_id)

    result = await db.execute(query)
    return result.scalars().all()


async def create_book(db: AsyncSession, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)

    return db_book
