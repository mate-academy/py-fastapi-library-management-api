from sqlalchemy.orm import Session
from models import Book, Author
from schemas import BookCreate, AuthorCreate


def create_book(db: Session, book:BookCreate):
    if db.query(Book).filter(Book.title == book.title, Book.author_id == book.author_id).first():
        raise ValueError("Book with the same title and author already exists.")

    book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )


    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def get_books(db: Session, skip: int, limit: int, author_id: int = None):
    query = db.query(Book)
    if author_id:
        query = query.filter(Book.author_id == author_id)
    return query.offset(skip).limit(limit).all()


def create_author(db: Session, author: AuthorCreate):
    if db.query(Author).filter(Author.name == author.name).first():
        raise ValueError("Author with the same name already exists.")

    author = Author(
        name = author.name,
        bio = author.bio,
    )

    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def get_author(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()


def get_authors(db: Session, skip: int, limit: int):
    return db.query(Author).offset(skip).limit(limit).all()
