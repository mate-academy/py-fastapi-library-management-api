from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from library_service.crud import create_book, get_book_list
from library_service.database import get_db
from library_service.schemas import BookCreateSchema, BookQueryParamsSchema

router = APIRouter()


@router.post("/")
async def add_book(
        data: BookCreateSchema,
        db: AsyncSession = Depends(get_db)
):
    result = create_book(data, db)
    return result


@router.get("/")
async def read_books(
        page: int = Query(1, ge=1, description="Page number (1-based index)"),
        per_page: int = Query(10, ge=1, le=20, description="Number of items per page"),
        params: BookQueryParamsSchema = Depends(),
        db: AsyncSession = Depends(get_db),
):
    result = await get_book_list(page, per_page, params, db)
    return result


@router.get("/{book_id}/")
async def get_book_detail(
        book_id: int,
        db: AsyncSession = Depends(get_db),
):
    result = await get_book_detail(book_id, db)
    return result
