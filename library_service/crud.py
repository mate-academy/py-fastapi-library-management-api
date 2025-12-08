from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from library_service.models import AuthorModel, BookModel
from library_service.schemas import (
    AuthorCreateSchema,
    AuthorListItemSchema,
    AuthorListResponseSchema,
    AuthorDetailSchema, BookCreateSchema, BookDetailSchema, BookQueryParamsSchema, BookListItemSchema,
    BookListResponseSchema
)


async def create_author(
        data: AuthorCreateSchema,
        db: AsyncSession
):
    existing_stmt = select(AuthorModel).where(
        (AuthorModel.name == data.name)
    )
    existing_result = await db.execute(existing_stmt)
    existing_author = existing_result.scalars().first()

    if existing_author:
        raise HTTPException(
            status_code=409,
            detail="Author already exists"
        )

    new_author = AuthorModel(
        name=data.name,
        bio=data.bio,
    )

    db.add(new_author)
    await db.commit()
    await db.refresh(new_author)

    return new_author


async def get_author_list(
        page: int,
        per_page: int,
        db: AsyncSession,
):

    offset = (page - 1) * per_page

    count_stmt = select(func.count(AuthorModel.id))
    result_count = await db.execute(count_stmt)
    total_items = result_count.scalar() or 0

    if not total_items:
        raise HTTPException(status_code=404, detail="No authors found.")

    order_by = AuthorModel.default_order_by()
    stmt = select(AuthorModel)

    if order_by:
        stmt = stmt.order_by(*order_by)

    stmt = stmt.offset(offset).limit(per_page)

    result_authors = await db.execute(stmt)
    authors = result_authors.scalars().all()

    if not authors:
        raise HTTPException(status_code=404, detail="No authors found.")

    author_list = [AuthorListItemSchema.model_validate(author) for author in authors]

    total_pages = (total_items + per_page - 1) // per_page

    response = AuthorListResponseSchema(
        authors=author_list,
        prev_page=f"/library_service/authors/?page={page - 1}&per_page={per_page}" if page > 1 else None,
        next_page=f"/library_service/authors/?page={page + 1}&per_page={per_page}" if page < total_pages else None,
        total_pages=total_pages,
        total_items=total_items,
    )
    return response


async def get_author_by_id(
        author_id: int,
        db: AsyncSession
) -> AuthorDetailSchema:

    stmt = (
        select(AuthorModel)
        .options(
            selectinload(AuthorModel.books),
        )
        .where(AuthorModel.id == author_id)
    )

    result = await db.execute(stmt)
    author = result.scalars().first()

    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author with the given ID was not found."
        )

    return AuthorDetailSchema.model_validate(author)


async def create_book(
        data: BookCreateSchema,
        db: AsyncSession
):
    existing_stmt = select(BookModel).where(
        (BookModel.title == data.title)
    )
    existing_result = await db.execute(existing_stmt)
    existing_book = existing_result.scalars().first()

    if existing_book:
        raise HTTPException(
            status_code=409,
            detail="Book already exists",
        )

    try:
        author_stmt = select(AuthorModel).where(AuthorModel.name == data.author)
        author_result = await db.execute(author_stmt)
        author = author_result.scalars().first()
        if not author:
            author = AuthorModel(name=data.author)
            db.add(author)
            await db.flush()

        book = BookModel(
            title=data.title,
            summary=data.summary,
            publication_date=data.publication_date,
            author=author,
        )

        db.add(book)
        await db.commit()
        await db.refresh(book)

        return BookDetailSchema.model_validate(book)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Invalid input data.")


async def get_book_list(
        page: int,
        per_page: int,
        params: BookQueryParamsSchema,
        db: AsyncSession,
):
    offset = (page - 1) * per_page

    count_stmt = select(func.count(BookModel.id))
    result_count = await db.execute(count_stmt)
    total_items = result_count.scalar() or 0

    if not total_items:
        raise HTTPException(status_code=404, detail="No books found.")

    order_by = BookModel.default_order_by()
    stmt = select(BookModel)

    if order_by:
        stmt = stmt.order_by(*order_by)

    if params.author_id is not None:
        stmt = stmt.where(BookModel.author_id == params.author_id)

    stmt = stmt.offset(offset).limit(per_page)

    result_books = await db.execute(stmt)
    books = result_books.scalars().all()

    if not books:
        raise HTTPException(status_code=404, detail="No books found.")

    book_list = [BookListItemSchema.model_validate(book) for book in books]

    total_pages = (total_items + per_page - 1) // per_page

    response = BookListResponseSchema(
        books=book_list,
        prev_page=f"/library_service/books/?page={page - 1}&per_page={per_page}" if page > 1 else None,
        next_page=f"/library_service/books/?page={page + 1}&per_page={per_page}" if page < total_pages else None,
        total_pages=total_pages,
        total_items=total_items,
    )
    return response


async def get_book_by_id(
        book_id: int,
        db: AsyncSession
):
    stmt = (
        select(BookModel)
        .options(
            joinedload(BookModel.author),
        )
        .where(BookModel.id == book_id)
    )

    result = await db.execute(stmt)
    book = result.scalars().first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book with the given ID was not found."
        )

    return BookDetailSchema.model_validate(book)
