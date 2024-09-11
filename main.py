from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import models
import schemas
from database import SessionLocal

app = FastAPI()


async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


@app.get("/authors/", response_model=list[schemas.Author])
async def read_authors(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> list:
    return await crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
async def read_author(
    author_id: int,
    db: AsyncSession = Depends(get_db)
) -> models.Author:
    db_author = await crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post(
    "/authors/",
    response_model=schemas.Author,
    status_code=status.HTTP_201_CREATED
)
async def create_author(
    author: schemas.AuthorCreate,
    db: AsyncSession = Depends(get_db)
) -> models.Author:
    db_author = await crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author with this name already exists")
    return await crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
async def read_books(
    db: AsyncSession = Depends(get_db),
    author_id: int = None,
    skip: int = 0,
    limit: int = 100,
) -> list:
    return await crud.get_books(db=db, author_id=author_id, skip=skip, limit=limit)


@app.post(
    "/books/",
    response_model=schemas.Book,
    status_code=status.HTTP_201_CREATED
)
async def create_book(
    book: schemas.BookCreate,
    db: AsyncSession = Depends(get_db)
) -> models.Book:
    return await crud.create_book(db=db, book=book)
