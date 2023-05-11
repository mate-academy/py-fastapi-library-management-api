from datetime import date
from typing import Type, List, Dict, Any, Sequence

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from sqlalchemy.orm import selectinload

from models import Author, Book


async def get_authors(db: AsyncSession, skip: int = 0, limit: int = 5) -> list[dict[str, list[dict[str, Any]] | Any]]:
    stmt = (
        select(models.Author)
        .options(selectinload(models.Author.books))
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    authors = result.scalars().all()
    return [
        {
            "id": author.id,
            "name": author.name,
            "bio": author.bio,
            "books": [
                {
                    "id": book.id,
                    "title": book.title,
                    "summary": book.summary,
                    "publication_date": book.publication_date,
                    "author_id": book.author_id,
                }
                for book in author.books
            ],
        }
        for author in authors
    ]


async def get_author(db: AsyncSession, author_id: int) -> dict:
    stmt = (
        select(models.Author)
        .options(selectinload(models.Author.books))
        .where(models.Author.id == author_id)
    )
    result = await db.execute(stmt)
    author = result.scalars().first()
    return {
        "id": author.id,
        "name": author.name,
        "bio": author.bio,
        "books": [
            {
                "id": book.id,
                "title": book.title,
                "summary": book.summary,
                "publication_date": book.publication_date,
                "author_id": book.author_id,
            }
            for book in author.books
        ],
    }


async def create_author(db: AsyncSession, author: schemas.AuthorCreate) -> schemas.Author:
    db_author = models.Author(**author.dict())
    db.add(db_author)
    await db.commit()
    await db.refresh(db_author)
    return db_author


async def update_author(
    db: AsyncSession,
    author_id: int,
    name: str = None,
    bio: str = None,
) -> Type[Author] | None:
    db_author = await db.get(models.Author, author_id)
    if name:
        db_author.name = name
    if bio:
        db_author.bio = bio
    await db.commit()
    await db.refresh(db_author)
    return db_author


async def delete_author(db: AsyncSession, author_id: int) -> Type[Author] | None:
    db_author = await db.get(models.Author, author_id)
    await db.delete(db_author)
    await db.commit()
    return db_author


async def get_books(
    db: AsyncSession,
    skip,
    limit,
    author_id: int = None,
) -> Sequence[Row | RowMapping | Any]:
    stmt = select(models.Book).offset(skip).limit(limit)
    if author_id:
        stmt = stmt.where(models.Book.author_id == author_id)
    result = await db.execute(stmt)
    books = result.scalars().all()
    return books


async def get_book(db: AsyncSession, book_id: int) -> schemas.Book:
    stmt = select(models.Book).where(models.Book.id == book_id)
    result = await db.execute(stmt)
    book = result.scalars().first()
    return book


async def create_book(db: AsyncSession, book: schemas.BookCreate) -> schemas.Book:
    db_book = models.Book(**book.dict())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book


async def update_book(
    db: AsyncSession,
    book_id: int,
    title: str = None,
    summary: str = None,
    publication_date: date = None,
    author_id: int = None,
) -> Type[Book] | None:
    db_book = await db.get(models.Book, book_id)
    if title:
        db_book.title = title
    if summary:
        db_book.summary = summary
    if publication_date:
        db_book.publication_date = publication_date
    if author_id:
        db_book.author_id = author_id
    await db.commit()
    await db.refresh(db_book)
    return db_book


async def delete_book(db: AsyncSession, book_id: int) -> Type[Book] | None:
    db_book = await db.get(models.Book, book_id)
    await db.delete(db_book)
    await db.commit()
    return db_book
