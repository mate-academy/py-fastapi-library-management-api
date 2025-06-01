from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.database import models
from src.schemas.schemas import AuthorCreateSchema


async def get_all_authors(db: AsyncSession):
    result = await db.execute(
        select(models.DbAuthor).options(selectinload(models.DbAuthor.books))
    )
    return result.scalars().all()


async def get_author_by_id(db: AsyncSession, author_id: int):
    result = await db.execute(
        select(models.DbAuthor)
        .options(selectinload(models.DbAuthor.books))
        .where(models.DbAuthor.id == author_id)
    )
    return result.scalars().first()


async def create_author(db: AsyncSession, author: AuthorCreateSchema):
    db_author = models.DbAuthor(**author.model_dump())
    db.add(db_author)
    await db.commit()
    await db.refresh(db_author)
    return db_author
