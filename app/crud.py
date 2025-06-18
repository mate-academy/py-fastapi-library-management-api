from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Author, Book
from app.schemas import (
    AuthorDetailSchema,
    AuthorCreateSchema,
    AuthorUpdateSchema,
    AuthorCreateResponseSchema, BookCreateSchema, BookDetailSchema,
    BookUpdateSchema
)


async def create_author(
        session: AsyncSession,
        data: AuthorCreateSchema
) -> AuthorCreateResponseSchema:
    new_author = Author(**data.model_dump())
    session.add(new_author)
    await session.commit()
    await session.refresh(new_author)
    return AuthorCreateResponseSchema.model_validate(new_author)


async def get_all_authors(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 10
) -> list[AuthorDetailSchema]:
    result = await session.execute(
        select(Author)
        .options(selectinload(Author.books))
        .offset(skip)
        .limit(limit)
    )
    authors = result.scalars().all()
    return [AuthorDetailSchema.model_validate(author) for author in
            authors]


async def get_author(
        session: AsyncSession, author_id: int
) -> AuthorDetailSchema:
    result = await session.execute(
        select(Author)
        .options(selectinload(Author.books))
        .where(Author.id == author_id)
    )
    author = result.scalars().first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return AuthorDetailSchema.model_validate(author)


async def update_author(
        session: AsyncSession,
        author_id: int,
        data: AuthorUpdateSchema
) -> AuthorDetailSchema:
    result_get = await session.execute(
        select(Author)
        .options(selectinload(Author.books))
        .where(Author.id == author_id)
    )
    author = result_get.scalars().first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(author, key, value)

    await session.commit()
    await session.refresh(author)
    return AuthorDetailSchema.model_validate(author)


async def delete_author(
        session: AsyncSession,
        author_id: int
) -> None:
    result = await session.execute(
        select(Author).where(Author.id == author_id)
    )
    author = result.scalars().first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    await session.delete(author)
    await session.commit()


async def create_book(
        session: AsyncSession,
        data: BookCreateSchema
) -> BookDetailSchema:
    result = await session.execute(
        select(Author).where(Author.id == data.author_id)
    )
    author = result.scalars().first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    new_book = Book(**data.model_dump())
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return BookDetailSchema.model_validate(new_book)


async def get_all_books(
        session: AsyncSession,
        author_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 10
) -> list[BookDetailSchema]:
    stmt = select(Book)

    if author_id is not None:
        stmt = select(Book).where(Book.author_id == author_id)

    result = await session.execute(
        stmt.offset(skip).limit(limit)
    )
    books = result.scalars().all()
    return [
        BookDetailSchema.model_validate(book)
        for book in books
    ]


async def get_book(
        session: AsyncSession, book_id: int
) -> BookDetailSchema:
    result = await session.execute(
        select(Book)
        .where(Book.id == book_id)
    )
    book = result.scalars().first()
    if book:
        return BookDetailSchema.model_validate(book)
    else:
        raise HTTPException(status_code=404, detail="Book not found")


async def update_book(
        session: AsyncSession,
        book_id: int,
        data: BookUpdateSchema
) -> BookDetailSchema:
    result = await session.execute(
        select(Book).where(Book.id == book_id)
    )
    book = result.scalars().first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if data.author_id is not None:
        result = await session.execute(
            select(Author).where(Author.id == data.author_id)
        )
        author = result.scalars().first()
        if not author:
            raise HTTPException(
                status_code=404,
                detail="Incorrect author_id! Author not found"
            )

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(book, key, value)

    await session.commit()
    await session.refresh(book)
    return BookDetailSchema.model_validate(book)


async def delete_book(
        session: AsyncSession,
        book_id: int
) -> None:
    result = await session.execute(
        select(Book).where(Book.id == book_id)
    )
    book = result.scalars().first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    await session.delete(book)
    await session.commit()
