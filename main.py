from typing import List, Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends

import crud
import schemas
from database import get_async_session

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True})


async def paginate_parameters(
        offset: int = 0, limit: int = 100
) -> dict:
    return {"offset": offset, "limit": limit}


PaginateDep = Annotated[dict, Depends(paginate_parameters)]


@app.get("/")
async def root():
    return {"result": "hello world"}


@app.get("/authors/", response_model=List[schemas.Author])
async def read_authors(
    paginate_params: PaginateDep,
    name: str | None = None,
    session: AsyncSession = Depends(get_async_session)
) -> List[schemas.Author]:
    return await crud.get_authors(session=session, name=name, **paginate_params)


@app.get("/authors/{id}/", response_model=schemas.Author)
async def get_author(
        id: int,
        session: AsyncSession = Depends(get_async_session)
) -> schemas.Author:
    return await crud.retrieve_author(id=id, session=session)


@app.post("/authors/", response_model=schemas.Author)
async def create_author(
        author: schemas.AuthorCreate,
        session: AsyncSession = Depends(get_async_session)
) -> schemas.Author:
    return await crud.create_author(author=author, session=session)


@app.get("/books/", response_model=List[schemas.Book])
async def read_books(
        paginate_params: PaginateDep,
        title: str | None = None,
        author_id: int | None = None,
        session: AsyncSession = Depends(get_async_session)
) -> List[schemas.Book]:
    return await crud.get_books(
        session=session,
        author_id=author_id,
        title=title,
        **paginate_params
    )


@app.get("/books/{id}/", response_model=schemas.BookDetail)
async def get_book(
        id: int,
        session: AsyncSession = Depends(get_async_session)
) -> schemas.Book:
    return await crud.retrieve_book(id=id, session=session)


@app.post("/books/", response_model=schemas.Book)
async def create_book(
        book: schemas.BookCreate,
        session: AsyncSession = Depends(get_async_session)
) -> schemas.Book:
    return await crud.create_book(book=book, session=session)
