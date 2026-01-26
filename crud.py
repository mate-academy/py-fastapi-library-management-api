from sqlalchemy import select
from sqlalchemy.orm import Session
import models
import schemas


# #FB approach
# def create_author(db: Session, author: schemas.CreateAuthor) -> models.Author:
#     db_author = models.Author(name=author.name, bio=author.bio)
#     db.add(db_author)
#     db.commit()
#     db.refresh(db_author)
#     return db_author
#
#
# def get_all_authors(db: Session, skip: int = 0, limit: int = 10) -> list[models.Author]:
#     stmt = select(models.Author).offset(skip).limit(limit)
#     return db.scalars(stmt).all()
#
#
# # def get_author_by_id(db: Session, author_id: int) -> models.Author | None:  # alternative version
# #     return db.get(models.Author, author_id)
#
#
# def get_author_by_id(db: Session, author_id: int) -> models.Author | None:
#     stmt = select(models.Author).where(models.Author.id == author_id)
#     return db.scalar(stmt)
#     # return db.scalars(stmt).first() # the same if id is unique
#
#
# def get_author_by_name(db: Session, name: str) -> models.Author | None:
#     stmt = select(models.Author).where(models.Author.name == name)
#     return db.scalars(stmt).first()
#
#
# def create_book(db: Session, book: schemas.CreateBook) -> models.Book:
#     # db_book = models.Book(
#     #     title=book.title,
#     #     summary=book.summary,
#     #     publication_date=book.publication_date,
#     #     author_id=book.author_id,
#     # )
#     db_book = models.Book(**book.model_dump())  # modern approach
#     db.add(db_book)
#     db.commit()
#     db.refresh(db_book)
#     return db_book
#
#
# def get_book_list(db: Session, skip: int = 0, limit: int = 7) -> list[models.Book]:
#     stmt = select(models.Book).offset(skip).limit(limit)
#     return db.scalars(stmt).all()
#
#
# def get_filter_book_list(db: Session, author_id: int | None = None) -> list[models.Book]:
#     stmt = select(models.Book)
#     if author_id is not None:
#         stmt = stmt.where(models.Book.author_id == author_id)
#     return db.scalars(stmt).all()


class AuthorCRUD:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 10) -> list[models.Author]:
        stmt = select(models.Author).offset(skip).limit(limit)
        return db.scalars(stmt).all()

    @staticmethod
    def get_by_id(db: Session, author_id: int) -> models.Author | None:
        return db.get(models.Author, author_id)

    @staticmethod
    def get_by_name(db: Session, name: str) -> models.Author | None:
        stmt = select(models.Author).where(models.Author.name == name)
        return db.scalars(stmt).first()

    @staticmethod
    def create(db: Session, author: schemas.CreateAuthor) -> models.Author:
        db_author = models.Author(**author.model_dump())
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
        return db_author


class BookCRUD:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 7) -> list[models.Book]:
        stmt = select(models.Book).offset(skip).limit(limit)
        return db.scalars(stmt).all()

    @staticmethod
    def filter(db: Session, author_id: int | None = None) -> list[models.Book]:
        stmt = select(models.Book)
        if author_id is not None:
            stmt = stmt.where(models.Book.author_id == author_id)
        return db.scalars(stmt).all()

    @staticmethod
    def create(db: Session, book: schemas.CreateBook) -> models.Book:
        db_book = models.Book(**book.model_dump())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book


author_crud = AuthorCRUD()
book_crud = BookCRUD()
