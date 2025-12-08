from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from library_service.crud import create_book, get_book_list, get_book_by_id
from library_service.database import get_db
from library_service.schemas import BookCreateSchema, BookQueryParamsSchema

router = APIRouter()


@router.post("/")
async def add_book(
        data: BookCreateSchema,
        db: AsyncSession = Depends(get_db)
):
    result = await create_book(data, db)
    return result


@router.get("/")
async def read_books(
        skip: int,
        limit: int,
        db: AsyncSession = Depends(get_db),
        params: BookQueryParamsSchema = Depends(),
):
    result = await get_book_list(skip, limit, params, db)
    return result


@router.get("/{book_id}")
async def get_book_detail(
        book_id: int,
        db: AsyncSession = Depends(get_db),
):
    result = await get_book_by_id(book_id, db)
    return result
