from sqlalchemy.orm import Session
import models
import schemas
from security import get_password_hash


def get_author_list(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        name=None
):
    queryset = db.query(models.Author).offset(skip).limit(limit).all()
    if name:
        return queryset.filter(models.Author.name.icontains(name)).all()
    return queryset


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def delete_author(db: Session, author_id: int):
    db.query(models.Author).filter(models.Author.id == author_id).delete()
    db.commit()


def get_book_list(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        title=None,
        author_id=None
):
    queryset = db.query(models.Book).offset(skip).limit(limit).all()
    if title:
        return queryset.filter(models.Book.title.icontains(title)).all()
    if author_id:
        return queryset.filter(models.Book.author_id == author_id).first()
    return queryset


def get_book(db: Session, book_id: int):
        return db.query(models.Book).filter(models.Book.id == book_id).first()


def delete_book(db: Session, book_id: int):
    db.query(models.Book).filter(models.Book.id == book_id).delete()
    db.commit()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def create_user(db: Session, user: schemas.User):
    hashed_password = get_password_hash(user.hashed_password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
