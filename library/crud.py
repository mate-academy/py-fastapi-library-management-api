from sqlalchemy import select

from library.models import Author, Book


def create_author(db, AuthorCreate):
    author = Author(name=AuthorCreate.name, bio=AuthorCreate.bio)

    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def get_authors(db, skip, limit):
    queryset = select(Author).offset(skip).limit(limit)
    authors = db.scalars(queryset).all()
    return authors


def get_author(db, author_id):
    author = db.scalar(select(Author).where(Author.id == author_id))
    return author


def create_book(db, BookCreate, author_id):
    book = Book(
        title=BookCreate.title,
        summary=BookCreate.summary,
        publication_date=BookCreate.publication_date,
        author_id=author_id,
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


def get_books(db, skip, limit, author_id):
    queryset = select(Book)

    if author_id:
        queryset = queryset.where(Book.author_id == author_id)

    queryset = queryset.offset(skip).limit(limit)

    books = db.scalars(queryset).all()
    return books


def get_book(db, book_id):
    book = db.scalar(select(Book).where(Book.id == book_id))
    return book
