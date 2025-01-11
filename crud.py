from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session):
    db_authors = db.query(models.DBAuthor).all()
    schema_authors = []
    for author in db_authors:
        author = schemas.Author(
            id=author.id,
            name=author.name,
            bio=author.bio,
            books=[
                book.id
                for book in author.books
            ]
        )
        schema_authors.append(author)
    return schema_authors


def get_author(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def get_author_by_name(db: Session, name: str):
    return (
        db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()
    )


def create_author(
        db: Session,
        author: schemas.AuthorCreate
) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,

    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def update_author(
        db: Session,
        db_author: models.DBAuthor,
        author: schemas.Author
) -> models.DBAuthor:
    for key, value in author.dict().items():
        if not (getattr(db_author, key) == getattr(author, key)):
            setattr(db_author, key, value)
    db.commit()
    return db_author


def delete_author(db: Session, author_id: int) -> models.DBAuthor:
    db_author = get_author(db, author_id)
    db.delete(db_author)
    db.commit()

    return db_author


def get_all_books(db: Session):
    db_books = db.query(models.DBBook).all()
    schema_books = [
        schemas.BookDetail(
            id=db_book.id,
            title=db_book.title,
            summary=db_book.summary,
            publication_date=db_book.publication_date,
            author_id=db_book.author_id
        )
        for db_book in db_books
    ]
    return schema_books


def get_book(db: Session, book_id: int):
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def get_book_by_title(db: Session, title: str):
    return (
        db.query(models.DBBook).filter(models.DBBook.title == title).first()
    )


def create_book(
        db: Session,
        book: schemas.BookCreate
) -> schemas.BookDetail:
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return schemas.BookDetail(
        id=db_book.id,
        title=db_book.title,
        summary=db_book.summary,
        publication_date=db_book.publication_date,
        author_id=db_book.author_id
    )


def update_book(
        db: Session,
        db_book: models.DBBook,
        book: schemas.BookDetail
) -> models.DBBook:
    for key, value in book.dict().items():
        if not (getattr(db_book, key) == getattr(book, key)):
            setattr(db_book, key, value)
    db.commit()
    return db_book


def delete_book(db: Session, book_id: int) -> models.DBBook:
    db_book = get_book(db, book_id)
    db.delete(db_book)
    db.commit()

    return db_book
