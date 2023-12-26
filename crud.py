from sqlalchemy.orm import Session, joinedload
import models
import schemas


def get_authors(db: Session, skip: int, limit: int = 100) -> list[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int) -> models.Author:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_author_by_name(db: Session, name: str) -> models.Author:
    return db.query(models.Author).filter(models.Author.name == name).first()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    # db_author = models.Author(
    #     name=author.name,
    #     bio=author.bio,
    # )
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(
        db: Session,
        author_id: int,
        updated_author: schemas.AuthorUpdate
) -> models.Author:
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if db_author:
        for key, value in updated_author.model_dump().items():
            setattr(db_author, key, value)
        db.commit()
        db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int) -> models.Author:
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if db_author:
        db.delete(db_author)
        db.commit()
    return db_author


def get_books(
        db: Session,
        skip: int,
        limit: int = 100,
        author_id: int | None = None
) -> list[models.Book]:
    query = db.query(models.Book)
    if author_id:
        query = query.filter(models.Book.author_id == author_id)
    return query.offset(skip).limit(limit).all()


def get_book_by_id(db: Session, book_id: int) -> models.Book:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book_with_author(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, updated_book: schemas.BookUpdate) -> models.Book:
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        for key, value in updated_book.model_dump().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> models.Book:
    db_book = db.query(models.Book).options(
        joinedload(models.Book.author)
    ).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book
