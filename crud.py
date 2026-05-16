from sqlalchemy import select
from models import Author, Book
from schemas import AuthorCreate, BookCreate


def get_author(db, author_id: int):
    result = db.execute(select(Author).where(Author.id == author_id))
    author = result.scalars().first()
    return author

def get_authors(db, skip: int = 0, limit: int = 10):
    result = db.execute(select(Author).offset(skip).limit(limit))
    authors = result.scalars().all()
    return authors

def create_author(db, author: AuthorCreate):
    db_author = Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_books(db, skip: int = 0, limit: int = 10, author_id: int = None):
    query = select(Book)
    if author_id:
        query = query.where(Book.author_id == author_id)
    result = db.execute(query.offset(skip).limit(limit))
    books = result.scalars().all()
    return books

def create_book(db, book: BookCreate):
    db_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
