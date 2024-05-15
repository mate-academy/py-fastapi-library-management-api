from abc import abstractmethod, ABC
from typing import List
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Author, Book


class AbstractDBManager(ABC):
    def __init__(self, session: Session) -> None:
        self.session = session

    @abstractmethod
    def get_all_items(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_single_item_by_id(self, item_id: int):
        pass

    @abstractmethod
    def create_new_item(self, item):
        pass

    @abstractmethod
    def validate_item(self, item) -> None:
        pass


class AuthorDBManager(AbstractDBManager):

    def get_all_items(self, skip: int, limit: int) -> List[Author]:
        return self.session.scalars(select(Author).offset(skip).limit(limit))

    def get_single_item_by_id(self, item_id: int) -> Author:
        try:
            return self.session.execute(select(Author).where(Author.id == item_id)).scalar_one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Author with such id does not exist")

    def get_item_by_name(self, name: str):
        try:
            return self.session.execute(select(Author).where(Author.name == name)).scalar_one()
        except NoResultFound:
            return None

    def create_new_item(self, item) -> Author:
        self.validate_item(item)
        try:
            with self.session as session:
                new_author = Author(name=item.name, bio=item.bio)
                session.add(new_author)
                session.commit()
                session.refresh(new_author)
                return new_author
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def validate_item(self, item) -> None:
        if len(item.name) > 255:
            raise HTTPException(status_code=400, detail="Name is too long")
        author = self.get_item_by_name(item.name)
        if author:
            raise HTTPException(status_code=400, detail=f"Author with such name already exists, id: {author.id}")


class BookDBManager(AbstractDBManager):
    def get_all_items(self, author_id: int | None, skip: int, limit: int) -> List[Book]:
        query = select(Book).offset(skip).limit(limit)
        if author_id:
            query = query.where(author_id == author_id)
        return self.session.scalars(query)

    def create_new_item(self, item):
        self.validate_item(item)
        try:
            with self.session as session:
                new_book = Book(title=item.title, summary=item.summary, publication_date=item.publication_date,
                                author_id=item.author_id)
                session.add(new_book)
                session.commit()
                session.refresh(new_book)
                return new_book
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def validate_item(self, item) -> None:
        self.validate_author(item.author_id)
        if len(item.title) > 255:
            raise HTTPException(status_code=400, detail="Title is too long")
        exiring_book = self.get_item_by_author_and_title(item.author_id, item.title)
        if exiring_book:
            raise HTTPException(status_code=400, detail=f"Book already exists, id: {exiring_book.id}")

    def get_item_by_author_and_title(self, author_id: int, title: str):
        try:
            return (self.session
                    .execute(select(Book).where(Book.title == title, Book.author_id == author_id)).scalar_one())
        except NoResultFound:
            return None

    def validate_author(self, author_id: int):
        manager = AuthorDBManager(self.session)
        manager.get_single_item_by_id(author_id)

    def get_single_item_by_id(self, item_id: int):
        pass
