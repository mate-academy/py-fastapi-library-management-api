from urllib.parse import urlencode

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import Base, engine, get_db

API_PREFIX = "/api/v1"

authors_router = APIRouter(prefix=f"{API_PREFIX}/authors", tags=["authors"])
books_router = APIRouter(prefix=f"{API_PREFIX}/books", tags=["books"])

Base.metadata.create_all(bind=engine)


def _build_pagination_params(
    page: int, per_page: int, author_id: int | None = None
) -> dict[str, int]:
    """
    Build query parameters for pagination URLs.

    Attributes:
        page (int): The page number.
        per_page (int): Number of items per page.
        author_id (int | None): Optional author ID for filtering.

    Returns:
        dict[str, int]: Dictionary with query parameters.
    """
    params = {"page": page, "per_page": per_page}

    if author_id:
        params["author_id"] = author_id

    return params


@authors_router.post(
    "/", response_model=schemas.Author, status_code=status.HTTP_201_CREATED
)
def create_author(
    author: schemas.AuthorBase, db: Session = Depends(get_db)
) -> schemas.Author:
    """
    Create a new author in the database.

    Attributes:
        author (schemas.AuthorBase): The author data to create.
        db (Session): The database session.

    Returns:
        schemas.Author: The created author with database-populated fields.

    Raises:
        HTTPException: If author with the same name already exists.
    """
    try:
        return crud.create_author(db, author)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author with this name already exists.",
        )


@authors_router.get("/", response_model=schemas.AuthorListResponse)
def get_authors(
    page: int = Query(1, gt=0),
    per_page: int = Query(10, gt=0, le=100),
    db: Session = Depends(get_db),
) -> schemas.AuthorListResponse:
    """
    Retrieve a paginated list of authors from the database.

    Attributes:
        page (int): The page number (1-based).
        per_page (int): Number of records per page.
        db (Session): The database session.

    Returns:
        schemas.AuthorListResponse: Paginated list of authors with navigation links.
    """
    authors, total_items, total_pages = crud.get_authors_with_pagination(
        db, page, per_page
    )

    prev_page_url = None
    next_page_url = None

    if page > 1:
        params = _build_pagination_params(page - 1, per_page)
        prev_page_url = f"{API_PREFIX}/authors?{urlencode(params)}"

    if page < total_pages:
        params = _build_pagination_params(page + 1, per_page)
        next_page_url = f"{API_PREFIX}/authors?{urlencode(params)}"

    return schemas.AuthorListResponse(
        authors=authors,
        prev_page=prev_page_url,
        next_page=next_page_url,
        total_pages=total_pages,
        total_items=total_items,
    )


@authors_router.get("/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)) -> schemas.Author:
    """
    Retrieve an author from the database by their ID.

    Attributes:
        author_id (int): The ID of the author to retrieve.
        db (Session): The database session.

    Returns:
        schemas.Author: The author if found.

    Raises:
        HTTPException: If author with given ID is not found.
    """
    author = crud.get_author_by_id(db, author_id)

    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with ID {author_id} not found.",
        )

    return author


@books_router.post(
    "/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED
)
def create_book(
    book: schemas.BookBase, author_id: int, db: Session = Depends(get_db)
) -> schemas.Book:
    """
    Create a new book in the database.

    Attributes:
        book (schemas.BookBase): The book data to create.
        author_id (int): The ID of the author who wrote the book.
        db (Session): The database session.

    Returns:
        schemas.Book: The created book with database-populated fields.

    Raises:
        HTTPException: If author is not found or book with these details already exists.
    """
    try:
        new_book = crud.create_book(db, book, author_id)

        if not new_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with ID {author_id} not found.",
            )

        return new_book
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with these details already exists.",
        )


@books_router.get("/", response_model=schemas.BookListResponse)
def get_books(
    page: int = Query(1, gt=0),
    per_page: int = Query(10, gt=0, le=100),
    author_id: int | None = None,
    db: Session = Depends(get_db),
) -> schemas.BookListResponse:
    """
    Retrieve a paginated list of books from the database.

    Attributes:
        page (int): The page number (1-based).
        per_page (int): Number of records per page.
        author_id (int | None): Optional ID of the author to filter books by.
        db (Session): The database session.

    Returns:
        schemas.BookListResponse: Paginated list of books with navigation links.

    Raises:
        HTTPException: If author_id is provided but author is not found.
    """
    if author_id:
        author = crud.get_author_by_id(db, author_id)

        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with ID {author_id} not found.",
            )

    books, total_items, total_pages = crud.get_books_with_pagination(
        db, page, per_page, author_id
    )

    prev_page_url = None
    next_page_url = None

    if page > 1:
        params = _build_pagination_params(page - 1, per_page, author_id)
        prev_page_url = f"{API_PREFIX}/books?{urlencode(params)}"

    if page < total_pages:
        params = _build_pagination_params(page + 1, per_page, author_id)
        next_page_url = f"{API_PREFIX}/books?{urlencode(params)}"

    return schemas.BookListResponse(
        books=books,
        prev_page=prev_page_url,
        next_page=next_page_url,
        total_pages=total_pages,
        total_items=total_items,
    )


app = FastAPI(title="Library Management API")
app.include_router(authors_router)
app.include_router(books_router)
