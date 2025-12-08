
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from library_service.database import get_db
from library_service.models import AuthorModel, BookModel
from library_service.schemas import (
    BookCreateSchema,
    BookDetailSchema,
    BookListItemSchema,
    BookListResponseSchema, BookQueryParamsSchema
)

router = APIRouter()


@router.post("/books/")
async def create_book(
        data: BookCreateSchema,
        db: AsyncSession = Depends(get_db)
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


@router.get("/books/")
async def get_book_list(
        page: int = Query(1, ge=1, description="Page number (1-based index)"),
        per_page: int = Query(10, ge=1, le=20, description="Number of items per page"),
        params: BookQueryParamsSchema = Depends(),
        db: AsyncSession = Depends(get_db),
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


@router.get("/books/{book_id}/")
async def get_book_by_id(
        book_id: int,
        db: AsyncSession = Depends(get_db),
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
