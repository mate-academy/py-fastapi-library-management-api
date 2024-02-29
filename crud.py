from sqlalchemy.orm import Session

import models
import schemas


def create_author(db: Session,
                  author_create: schemas.AuthorCreate,
                  ) -> models.DBAuthor:
    db_author = models.DBAuthor(**author_create.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author(db: Session,
               author_id: int,
               ) -> models.DBAuthor:
    return (db
            .query(models.DBAuthor)
            .filter(models.DBAuthor.id == author_id)
            .first()
            )


def get_author_by_name(db: Session,
                       name: str,
                       ) -> models.DBAuthor:
    return (db
            .query(models.DBAuthor)
            .filter(models.DBAuthor
                    .name == name)
            .first()
            )


def get_authors(db: Session,
                skip: int = 0,
                limit: int = 10,
                ) -> list[models.DBAuthor]:
    return (db
            .query(models.DBAuthor)
            .offset(skip)
            .limit(limit)
            .all()
            )


def update_author(db: Session,
                  author_id: int,
                  author_update:
                  schemas.AuthorCreate,
                  ) -> models.DBAuthor:
    db_author = get_author(db, author_id)
    for key, value in author_update.dict().items():
        setattr(db_author, key, value)
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session,
                  author_id: int,
                  ) -> models.DBAuthor:
    db_author = get_author(db, author_id)
    db.delete(db_author)
    db.commit()
    return db_author


def create_book(db: Session,
                book_create: schemas.BookCreate,
                ) -> models.DBBook:
    db_book = models.DBBook(**book_create.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session,
             book_id: int,
             ) -> models.DBBook:
    return (db
            .query(models.DBBook)
            .filter(models.DBBook.id == book_id)
            .first()
            )


def get_books_by_author(db: Session,
                        author_id: int,
                        ) -> list[models.DBBook]:
    return (db
            .query(models.DBBook)
            .filter(models.DBBook.author_id == author_id)
            .all()
            )


def get_books(db: Session,
              skip: int = 0,
              limit: int = 10,
              ) -> list[models.DBBook]:
    return (db
            .query(models.DBBook)
            .offset(skip)
            .limit(limit)
            .all()
            )


def update_book(db: Session,
                book_id: int,
                book_update: schemas.BookCreate,
                ) -> models.DBBook:
    db_book = get_book(db, book_id)
    for key, value in book_update.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session,
                book_id: int,
                ) -> models.DBBook:
    db_book = get_book(db, book_id)
    db.delete(db_book)
    db.commit()
    return db_book
