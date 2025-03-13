from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from crud.author import get_author, get_author_list, add_author
from schemas import Author, AuthorCreate


router = APIRouter()


@router.get("/", response_model=List[Author])
async def read_authors(db: AsyncSession = Depends(get_db)):
    authors = await get_author_list(db)
    return authors


@router.get("/{author_id}", response_model = Author)
async def read_author(author_id: int, db: AsyncSession = Depends(get_db)):
    author = await get_author(db=db,author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.post("/", response_model=AuthorCreate)
async def create_author(author: AuthorCreate, db: AsyncSession = Depends(get_db)):
    new_author = await add_author(db=db, author=author)
    return new_author
