from datetime import date

from database import get_async_session
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas
from users import auth_backend, fastapi_users, current_active_user

app = FastAPI()


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(schemas.UserRead, schemas.UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(schemas.UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(schemas.UserRead, schemas.UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get("/authors", response_model=list[schemas.Author])
async def get_authors(db: AsyncSession = Depends(get_async_session)):
    return await crud.get_authors(db=db)


@app.get("/authors/{author_id}", response_model=schemas.Author)
async def get_author(author_id: int, db: AsyncSession = Depends(get_async_session)):
    return await crud.get_author(db=db, author_id=author_id)


@app.post("/authors/create", response_model=schemas.Author)
async def create_author(
    author: schemas.AuthorCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(current_active_user),
):
    if current_user:
        return await crud.create_author(db=db, author=author)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")


@app.put("/authors/update/{author_id}", response_model=schemas.Author)
async def update_author(
    author_id: int,
    name: str = None,
    bio: str = None,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(current_active_user),
):
    if current_user:
        return await crud.update_author(
            db=db,
            author_id=author_id,
            name=name,
            bio=bio,
        )
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")


@app.delete("/authors/delete/{author_id}", response_model=schemas.Author)
async def delete_author(
    author_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(current_active_user),
):
    if current_user:
        return await crud.delete_author(db=db, author_id=author_id)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")


@app.get("/books", response_model=list[schemas.Book])
async def get_books(
    db: AsyncSession = Depends(get_async_session), skip: int = 0, limit: int = 5
):
    return await crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/books/{book_id}", response_model=schemas.Book)
async def get_book(book_id: int, db: AsyncSession = Depends(get_async_session)):
    return await crud.get_book(db=db, book_id=book_id)


@app.post("/books", response_model=schemas.Book)
async def create_book(
    book: schemas.BookCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(current_active_user),
):
    if current_user:
        return await crud.create_book(db=db, book=book)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")


@app.put("/books/update/{book_id}", response_model=schemas.Book)
async def update_book(
    book_id: int,
    title: str = None,
    author_id: int = None,
    publication_date: date = None,
    summary: str = None,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(current_active_user),
):
    if current_user:
        return await crud.update_book(
            db=db,
            book_id=book_id,
            title=title,
            author_id=author_id,
            publication_date=publication_date,
            summary=summary,
        )
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")


@app.delete("/books/delete/{book_id}", response_model=schemas.Book)
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(current_active_user),
):
    if current_user:
        return await crud.delete_book(db=db, book_id=book_id)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
