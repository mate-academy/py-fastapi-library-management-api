from sqlalchemy.orm import Session

import models
import schema


def get_list_authors(db: Session, skip: int, limit: int):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_detail_author(db: Session, pk: int):
    return db.query(models.Author).filter(models.Author.id == pk).first()


def post_list_author(
        db: Session,
        author: schema.AuthorBase
):
    author = models.Author(name=author.name,
                            bio=author.bio)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def get_list_books(db: Session, skip: int, limit: int):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_detail_book(db: Session, pk: int):
    return db.query(models.Book).filter(models.Book.author_id == pk).all()


def post_list_book(
        db: Session,
        book: schema.BookCreate
):
    book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
