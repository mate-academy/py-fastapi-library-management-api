from typing import Optional

from fastapi import FastAPI, APIRouter, Query
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app import crud
from app.database import get_async_session
from app.schemas import (
    AuthorCreateSchema,
    AuthorDetailSchema,
    AuthorUpdateSchema,
    AuthorCreateResponseSchema, BookCreateSchema, BookDetailSchema,
    BookUpdateSchema
)

app = FastAPI(
    title="Library management"
)
authors_router = APIRouter(prefix="/authors", tags=["authors"])
books_router = APIRouter(prefix="/books", tags=["books"])


@authors_router.post("", status_code=status.HTTP_201_CREATED)
async def create_author(
        data: AuthorCreateSchema,
        session: AsyncSession = Depends(get_async_session)
) -> AuthorCreateResponseSchema:
    """
        Creates author in library with incoming data
    """
    return await crud.create_author(session=session, data=data)


@authors_router.get("", response_model=list[AuthorDetailSchema])
async def get_all_authors(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1),
        session: AsyncSession = Depends(get_async_session)
) -> list[AuthorDetailSchema]:
    """
        Returns list of all authors in library
    """
    return await crud.get_all_authors(session=session, skip=skip, limit=limit)


@authors_router.get("/{author_id}", response_model=AuthorDetailSchema)
async def get_author_by_id(
        author_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> AuthorDetailSchema:
    """
        Returns author in library with particular ID
    """
    return await crud.get_author(session=session, author_id=author_id)


@authors_router.patch(
    "/{author_id}",
    status_code=status.HTTP_200_OK
)
async def update_author(
        author_id: int,
        data: AuthorUpdateSchema,
        session: AsyncSession = Depends(get_async_session)
) -> AuthorDetailSchema:
    """
        Fully or partially updates author's fields in library
    """
    return await crud.update_author(
        session=session,
        author_id=author_id,
        data=data
    )


@authors_router.delete(
    "/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_author_by_id(
        author_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> None:
    """
        Deletes author from the library
    """
    await crud.delete_author(session=session, author_id=author_id)


@books_router.post("", status_code=status.HTTP_201_CREATED)
async def create_book(
        data: BookCreateSchema,
        session: AsyncSession = Depends(get_async_session)
) -> BookDetailSchema:
    """
        Creates book in library with incoming data
    """
    return await crud.create_book(session=session, data=data)


@books_router.get("", response_model=list[BookDetailSchema])
async def get_all_books(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1),
        author_id: Optional[int] = Query(None),
        session: AsyncSession = Depends(get_async_session)
) -> list[BookDetailSchema]:
    """
        Returns list of all books in library
    """
    return await crud.get_all_books(
        session=session, skip=skip, limit=limit, author_id=author_id
    )


@books_router.get("/{book_id}", response_model=BookDetailSchema)
async def get_book_by_id(
        book_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> BookDetailSchema:
    """
        Returns book in library with particular ID
    """
    return await crud.get_book(session=session, book_id=book_id)


@books_router.patch("/{book_id}", response_model=BookDetailSchema)
async def update_book(
        book_id: int,
        data: BookUpdateSchema,
        session: AsyncSession = Depends(get_async_session)
) -> BookDetailSchema:
    """
        Fully or partially updates book's fields in library
    """
    return await crud.update_book(
        session=session, book_id=book_id, data=data
    )


@books_router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book_by_id(
        book_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> None:
    """
        Deletes book from library
    """
    await crud.delete_book(session=session, book_id=book_id)

app.include_router(authors_router)
app.include_router(books_router)
