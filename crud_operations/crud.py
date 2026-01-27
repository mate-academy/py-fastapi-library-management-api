from typing import List, Optional

from sqlmodel import select

from fastapi import APIRouter, Query, HTTPException, status

from database import SessionDep

from models import Book, Author

from schemas import BookUpdate, BookCreate, AuthorUpdate


router = APIRouter()


#book
@router.post("/books/", response_model=Book)
def create_book(book_data: BookCreate, session: SessionDep) -> Book:
    book = Book(**book_data.model_dump())
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.get("/books/", response_model=List[Book])
def read_books(
        session: SessionDep,

        # Pagination
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),

        # Filtering
        author_id: Optional[int] = Query(None),
) -> List[Book]:

    statement = select(Book)

    if author_id:
        statement = statement.where(Book.author_id == author_id)

    statement = statement.offset(offset).limit(limit)

    return session.exec(statement).all()


@router.put("/books/{book_id}", response_model=Book)
def update_book(
        book_id: int,
        book_data: BookUpdate,
        session: SessionDep,
) -> Book:
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book_data.model_dump(exclude_unset=True).items():
        setattr(book, key, value)

    session.commit()
    session.refresh(book)
    return book


@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT,)
def delete_book(
        book_id: int,
        session: SessionDep,
) -> None:

    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    session.delete(book)
    session.commit()


#author
@router.post("/author/", response_model=Author)
def create_author(author: Author, session: SessionDep) -> Author:
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@router.get("/authors/", response_model=List[Author])
def read_author(
        session: SessionDep,
        limit: int = Query(1, ge=1, le=100),
        offset: int = Query(0, ge=0),
) -> List[Author]:

    statement = select(Author).offset(offset).limit(limit)

    return session.exec(statement).all()


@router.get("/authors/{author_id}", response_model=Author)
def read_single_author(
        author_id: int,
        session: SessionDep,
) -> Author | HTTPException:

    if session.get(Author, author_id) is None:
        raise HTTPException(status_code=404, detail="Author not found")

    statement = select(Author).where(Author.id == author_id)

    return session.exec(statement).first()


@router.put("/author/{author_id}", response_model=Author)
def update_author(
        author_id: int,
        author_data: AuthorUpdate,
        session: SessionDep,
) -> Author:
    author = session.get(Author, author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    for key, value in author_data.model_dump(exclude_unset=True).items():
        setattr(author, key, value)

    session.commit()
    session.refresh(author)
    return author


@router.delete("/author/{author_id}", status_code=status.HTTP_204_NO_CONTENT,)
def delete_author(
        author_id: int,
        session: SessionDep,
) -> None:

    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    session.delete(author)
    session.commit()
