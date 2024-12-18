from sqlalchemy.orm import Session
from models import Author, Book
from schemas import AuthorCreate, BookCreate


# Створення автора
def create_author(db: Session, author: AuthorCreate):
    db_author = Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


# Отримання списку авторів
def get_authors(db: Session, skip: int, limit: int):
    return db.query(Author).offset(skip).limit(limit).all()


# Отримання автора за ID
def get_author_by_id(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()


# Створення книги
def create_book(db: Session, author_id: int, book: BookCreate):
    db_book = Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


# Отримання списку книг
def get_books(db: Session, skip: int, limit: int, author_id: int = None):
    query = db.query(Book)
    if author_id:
        query = query.filter(Book.author_id == author_id)
    return query.offset(skip).limit(limit).all()
