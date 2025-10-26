from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from crud import (
    create_author,
    create_book,
    delete_author,
    delete_book,
    get_author_by_id,
    get_authors_list,
    get_book_by_id,
    get_books_list,
    update_author,
    update_book,
)

from database import get_db, engine, Base
from schemas import (
    AuthorCreate,
    AuthorRetrieve,
    AuthorUpdate,
    BookCreate,
    BookRetrieve,
    BookUpdate,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

# /// GET ///
@app.get("/books/", response_model=List[BookRetrieve])
async def list_books(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    author_id: Optional[int] = None
) -> List[BookRetrieve]:
    books = await get_books_list(db=db, skip=skip, limit=limit, author_id=author_id)
    return [BookRetrieve.model_validate(book) for book in books]


@app.get("/authors/", response_model=List[AuthorRetrieve])
async def list_authors(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 10
) -> List[AuthorRetrieve]:
    authors = await get_authors_list(db=db, skip=skip, limit=limit)
    return [AuthorRetrieve.model_validate(author) for author in authors]


@app.get("/authors/{author_id}", response_model=AuthorRetrieve)
async def retrieve_author(
    author_id: int,
    db: AsyncSession = Depends(get_db),
) -> AuthorRetrieve:
    author = await get_author_by_id(db=db, pk=author_id)
    return AuthorRetrieve.model_validate(author)


@app.get("/books/{book_id}", response_model=BookRetrieve)
async def retrieve_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
) -> BookRetrieve:
    book = await get_book_by_id(db=db, pk=book_id)
    return BookRetrieve.model_validate(book)


# /// POST ///
@app.post("/authors/create/", response_model=AuthorRetrieve)
async def author_create(
    author_data: AuthorCreate,
    db: AsyncSession = Depends(get_db)
) -> AuthorRetrieve:
    author = await create_author(db=db, author_data=author_data)
    return AuthorRetrieve.model_validate(author)


@app.post("/books/create/", response_model=BookRetrieve)
async def create_book_endpoint(
    book_data: BookCreate,
    db: AsyncSession = Depends(get_db)
) -> BookRetrieve:
    book = await create_book(db=db, book_data=book_data)
    return BookRetrieve.model_validate(book)


# /// PUT ///
@app.put("/authors/update/{author_id}", response_model=AuthorRetrieve)
async def put_author(
    author_id: int,
    author_update_data: AuthorUpdate,
    db: AsyncSession = Depends(get_db),
) -> AuthorRetrieve:
    author = await update_author(
        db=db, pk=author_id,
        author_update_data=author_update_data
    )
    return AuthorRetrieve.model_validate(author)


@app.put("/books/update/{book_id}", response_model=BookRetrieve)
async def put_book(
    book_id: int,
    book_update_data: BookUpdate,
    db: AsyncSession = Depends(get_db),
) -> BookRetrieve:
    book = await update_book(
        db=db, pk=book_id,
        book_update_data=book_update_data
    )
    return BookRetrieve.model_validate(book)


# /// DELETE ///
@app.delete("/books/delete/{book_id}")
async def delete_book_endpoint(
    book_id: int, db: AsyncSession = Depends(get_db)
) -> dict:
    return await delete_book(db=db, pk=book_id)


@app.delete("/authors/delete/{author_id}")
async def delete_author_endpoint(
    author_id: int, db: AsyncSession = Depends(get_db)
) -> dict:
    return await delete_author(db=db, pk=author_id)
