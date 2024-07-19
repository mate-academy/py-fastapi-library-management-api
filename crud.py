from fastapi import Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.orm import subqueryload
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from database import get_async_session


def get_paginated(model: models, offset: int, limit: int):
    return select(model).offset(offset).limit(limit)


async def get_authors(
        name: str | None,
        limit: int,
        offset: int,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = get_paginated(models.DBAuthor, offset, limit)
    if name:
        stmt = stmt.where(models.DBAuthor.name.icontains(name))

    authors_list = await session.execute(stmt)
    return [author[0] for author in authors_list.fetchall()]


async def retrieve_author(
        id: int,
        session: AsyncSession = Depends(get_async_session),
):
    stmt = select(models.DBAuthor).filter(models.DBAuthor.id == id).options(
        subqueryload(models.DBAuthor.books)
    )
    author = await session.execute(stmt)
    if not author.first():
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )
    return author.first()[0]


async def create_author(
        author: schemas.AuthorCreate,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(models.DBAuthor).values(
        name=author.name,
        bio=author.bio,
    )
    result = await session.execute(stmt)
    await session.commit()
    resp = {**author.model_dump(), "id": result.lastrowid}
    return resp


async def create_book(
        book: schemas.BookCreate,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = select(models.DBAuthor).where(models.DBAuthor.id == book.author_id)
    author = await session.execute(stmt)

    if not author.first():
        raise HTTPException(
            status_code=404,
            detail="There are no such author"
        )

    stmt = insert(models.DBBook).values(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )

    result = await session.execute(stmt)
    await session.commit()
    resp = {**book.model_dump(), "id": result.lastrowid}
    return resp


async def retrieve_book(
        id: int,
        session: AsyncSession = Depends(get_async_session),
):
    stmt = select(models.DBBook).filter(models.DBBook.id == id).options(subqueryload(models.DBBook.author))
    book = await session.execute(stmt)
    if not book.first():
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    return book.first()[0]


async def get_books(
        title: str | None,
        author_id: int | None,
        limit: int,
        offset: int,
        session: AsyncSession = Depends(get_async_session),
):
    stmt = get_paginated(models.DBBook, offset, limit)

    if title:
        stmt = stmt.where(models.DBBook.title.icontains(title))
    if author_id:
        stmt = stmt.where(models.DBBook.author_id == author_id)

    books_list = await session.execute(stmt)
    return [book[0] for book in books_list.fetchall()]
