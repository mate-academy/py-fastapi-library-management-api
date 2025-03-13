from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas


async def get_author_list(db: AsyncSession):
    query = select(models.Author).options(selectinload(models.Author.books))
    result = await db.execute(query)
    authors = result.scalars().all()
    return authors


async def get_author(db: AsyncSession, author_id: int):
    query = (
        select(models.Author)
        .options(selectinload(models.Author.books))
        .where(models.Author.id == author_id)
    )

    result = await db.execute(query)

    author = result.scalar_one_or_none()

    return author


async def add_author(db: AsyncSession, author: schemas.AuthorCreate):
    query = insert(models.Author).values(
        name=author.name,
        bio=author.bio,
    )

    result = await db.execute(query)

    await db.commit()

    response = {**author.model_dump(), "id": result.lastrowid}

    return response
