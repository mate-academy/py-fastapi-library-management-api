from sqlalchemy.orm import Query, Session

from app import models, schemas


def _paginate_query(query: Query, page: int, per_page: int) -> tuple[list, int, int]:
    """
    Helper function to handle pagination on any query.

    Attributes:
        query (Query): The SQLAlchemy query to paginate.
        page (int): The page number (1-based).
        per_page (int): Number of records per page.

    Returns: tuple[list, int, int]: A tuple containing:
        - List of models for the current page.
        - Total number of items.
        - Total number of pages.
    """
    total_items = query.count()
    total_pages = (total_items + per_page - 1) // per_page

    offset = (page - 1) * per_page
    items = query.offset(offset).limit(per_page).all()

    return items, total_items, total_pages


def create_author(db: Session, author: schemas.AuthorBase) -> models.Author:
    """
    Create a new author in the database.

    Attributes:
        db (Session): The database session.
        author (schemas.AuthorBase): The author data to create.

    Returns:
        models.Author: The created author model with database-populated fields.
    """
    new_author = models.Author(**author.model_dump())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def get_author_by_id(db: Session, author_id: int) -> models.Author | None:
    """
    Retrieve an author from the database by their ID.

    Attributes:
        db (Session): The database session.
        author_id (int): The ID of the author to retrieve.

    Returns:
        models.Author | None: The author model if found, None otherwise.
    """
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_authors_with_pagination(
    db: Session, page: int, per_page: int
) -> tuple[list, int, int]:
    """
    Retrieve a paginated list of authors from the database.

    Attributes:
        db (Session): The database session.
        page (int): The page number (1-based).
        per_page (int): Number of records per page.

    Returns: tuple[list, int, int]: A tuple containing:
        - List of Author models for the current page.
        - Total number of authors in the database.
        - Total number of pages.
    """
    query = db.query(models.Author)

    return _paginate_query(query, page, per_page)


def create_book(
    db: Session, book: schemas.BookBase, author_id: int
) -> models.Book | None:
    """
    Create a new book in the database.

    Attributes:
        db (Session): The database session.
        book (schemas.BookBase): The book data to create.
        author_id (int): The ID of the author who wrote the book.

    Returns:
        models.Book | None: The created book model with database-populated fields,
            or None if author with given ID doesn't exist.
    """
    author = get_author_by_id(db, author_id)

    if not author:
        return None

    new_book = models.Book(**book.model_dump(), author_id=author_id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_books_with_pagination(
    db: Session, page: int, per_page: int, author_id: int | None = None
) -> tuple[list, int, int]:
    """
    Retrieve a paginated list of books from the database.
    If author_id is provided, returns only books by that author.

    Attributes:
        db (Session): The database session.
        page (int): The page number (1-based).
        per_page (int): Number of records per page.
        author_id (int | None): Optional ID of the author to filter books by.

    Returns: tuple[list, int, int]: A tuple containing:
        - List of Book models for the current page.
        - Total number of books (filtered by author if specified).
        - Total number of pages.
    """
    query = db.query(models.Book)

    if author_id:
        query = query.filter(models.Book.author_id == author_id)

    return _paginate_query(query, page, per_page)
