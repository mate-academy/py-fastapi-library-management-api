from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from models import Base, Author, Book
from schemas import (
    AuthorCreateSchema,
    AuthorReadSchema,
    BookCreateSchema,
    BookReadSchema
)
from crud import (
    create_author,
    get_author_by_id,
    create_book,
)
from database import DATABASE_URL


engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI(title="Authors & Books API")


@app.post(
    "/authors/",
    response_model=AuthorReadSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_author_endpoint(
    author: AuthorCreateSchema,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await create_author(db, author)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exists"
        )


@app.get("/authors/", response_model=List[AuthorReadSchema])
async def list_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Author)
        .offset(skip)
        .limit(limit)
        .options(selectinload(Author.books))
    )
    authors = result.scalars().all()
    return authors


@app.get("/authors/{author_id}", response_model=AuthorReadSchema)
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)):
    author = await get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post(
    "/books/",
    response_model=BookReadSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_book_endpoint(
    book: BookCreateSchema,
    db: AsyncSession = Depends(get_db)
):
    author = await get_author_by_id(db, book.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return await create_book(db, book)


@app.get("/books/", response_model=List[BookReadSchema])
async def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    author_id: Optional[int] = Query(
        None,
        description="Filter books by author ID"
    ),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Book)
    if author_id is not None:
        stmt = stmt.where(Book.author_id == author_id)
    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    books = result.scalars().all()
    return books


@app.on_event("startup")
async def on_startup():
    await init_db()
