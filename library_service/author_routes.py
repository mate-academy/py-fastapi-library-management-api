from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from library_service.crud import create_author, get_author_list, get_author_by_id
from library_service.database import get_db
from library_service.schemas import AuthorCreateSchema, AuthorDetailSchema

router = APIRouter()


@router.post("/")
async def add_author(
        data: AuthorCreateSchema,
        db: AsyncSession = Depends(get_db)
):
    result = await create_author(data, db)
    return result


@router.get("/")
async def read_authors(
        skip: int,
        limit: int,
        db: AsyncSession = Depends(get_db),
):

    result = await get_author_list(skip, limit, db)
    return result


@router.get("/{author_id}")
async def get_author_detail(
        author_id: int,
        db: AsyncSession = Depends(get_db),
) -> AuthorDetailSchema:

    result = await get_author_by_id(author_id, db)
    return result
