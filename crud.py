from sqlalchemy.orm import Session

import models
import schemas


def get_author_list(
    db: Session,
    search_name: str = None,
    sorting_column: str = None,
    ascending: bool = True
):
    queryset = db.query(models.DBAuthor)
    if search_name:
        queryset = queryset.filter(
            models.DBAuthor.name.ilike(f"%{search_name}%")
        )

    if sorting_column:
        column = getattr(models.DBAuthor, sorting_column)
        if ascending:
            queryset = queryset.order_by(column)
        else:
            queryset = queryset.order_by(column.desc())

    return queryset.all()


def get_author_by_name(db: Session, name: str):
    return (
        db.query(models.DBAuthor).
        filter(models.DBAuthor.name == name).first()
    )


def get_author_by_id(db: Session, author_id: int):
    return (
        db.query(models.DBAuthor).
        filter(models.DBAuthor.id == author_id).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def update_author(db: Session, author: schemas.AuthorCreate, author_id: int):
    author_update = (
        db.query(models.DBAuthor).
        filter(models.DBAuthor.id == author_id).first()
    )
    author_update.name = author.name
    author_update.bio = author.bio
    db.add(author_update)
    db.commit()
    db.refresh(author_update)

    return author_update


def partial_update_author(
    db: Session, author: schemas.AuthorPartialUpdate, author_id: int
):
    author_update = (
        db.query(models.DBAuthor).
        filter(models.DBAuthor.id == author_id).first()
    )
    if author.name:
        author_update.name = author.name
    if author.bio:
        author_update.bio = author.bio
    db.add(author_update)
    db.commit()
    db.refresh(author_update)

    return author_update


def delete_author(db: Session, author_id: int):
    author = (
        db.query(models.DBAuthor).
        filter(models.DBAuthor.id == author_id).first()
    )
    author_books = (
        db.query(models.DBBook).
        filter(models.DBBook.author_id == author_id).all()
    )
    for book in author_books:
        db.delete(book)
    db.delete(author)
    db.commit()
    return {"message": "Author deleted successfully"}


def get_book_list(
    db: Session,
    author_id: int = None,
    book_title: str = None,
    sorting_column: str = None,
    ascending: bool = True
):
    queryset = db.query(models.DBBook)
    if author_id:
        queryset = queryset.filter(models.DBBook.author_id == author_id)

    if book_title:
        queryset = queryset.filter(
            models.DBBook.title.ilike(f"%{book_title}%")
        )

    if sorting_column:
        column = getattr(models.DBBook, sorting_column)
        if ascending:
            queryset = queryset.order_by(column)
        else:
            queryset = queryset.order_by(column.desc())

    return queryset.all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_book_by_id(db: Session, book_id: int):
    return (
        db.query(models.DBBook).
        filter(models.DBBook.id == book_id).first()
    )


def update_book(db: Session, book: schemas.BookCreate, book_id: int):
    book_update = (
        db.query(models.DBBook).
        filter(models.DBBook.id == book_id).first()
    )
    book_update.title = book.title
    book_update.summary = book.summary
    book_update.publish_date = book.publication_date
    book_update.author_id = book.author_id
    db.add(book_update)
    db.commit()
    db.refresh(book_update)

    return book_update


def partial_update_book(db: Session, book: schemas.BookPartialUpdate, book_id: int):
    book_update = (
        db.query(models.DBBook).
        filter(models.DBBook.id == book_id).first()
    )
    if book.title:
        book_update.title = book.title
    if book.summary:
        book_update.summary = book.summary
    if book.publication_date:
        book_update.publication_date = book.publication_date
    if book.author_id:
        book_update.author_id = book.author_id
    db.add(book_update)
    db.commit()
    db.refresh(book_update)

    return book_update


def delete_book(db: Session, book_id: int):
    book = (
        db.query(models.DBBook).
        filter(models.DBBook.id == book_id).first()
    )
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}
