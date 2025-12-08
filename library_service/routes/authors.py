from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from library_service.database import get_db
from library_service.models import AuthorModel
from library_service.schemas import (
    AuthorCreateSchema,
    AuthorListItemSchema,
    AuthorListResponseSchema,
    AuthorDetailSchema
)

router = APIRouter()


@router.post("/authors/")
async def create_author(
        data: AuthorCreateSchema,
        db: AsyncSession = Depends(get_db)
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


@router.get("/authors/")
async def get_author_list(
        page: int = Query(1, ge=1, description="Page number (1-based index)"),
        per_page: int = Query(10, ge=1, le=20, description="Number of items per page"),
        db: AsyncSession = Depends(get_db),
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


@router.get("/authors/{author_id}/")
async def get_author_by_id(
        author_id: int,
        db: AsyncSession = Depends(get_db),
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
