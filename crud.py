from fastapi import HTTPException, Response
from sqlalchemy.orm import Session
from starlette import status

from models import DBAuthor, DBBook
from schemas import BookNoId


def get_many(db_session: Session, db_model):
    return db_session.query(db_model).all()


def get_one(ident: int, db_session: Session, db_model):
    return db_session.get(db_model, ident)


def add_item(db_session: Session, item_data, db_model):
    new_item = db_model(**item_data.dict())

    db_session.add(new_item)
    db_session.commit()
    db_session.refresh(new_item)

    return new_item


def update_item(ident: int, db_session: Session, update_data, db_model):
    db_session.query(db_model).filter(db_model.id == ident).update(update_data.dict())
    db_session.commit()

    return db_session.get(db_model, ident)


def delete_item(ident: int, db_session: Session, db_model):
    obj = db_session.get(db_model, ident)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No item with this id: {ident} found')
    db_session.delete(obj)
    db_session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def get_books(db_session: Session, author_ids: str | None = None):
    queryset = db_session.query(DBBook)

    if author_ids:
        queryset = queryset.filter(
            DBBook.author_id.in_([int(num) for num in author_ids.split(",")])
        )
    return queryset.all()


def add_book(db_session: Session, book_data: BookNoId):
    data = book_data.dict()
    author_id = data["author_id"]
    author = db_session.get(DBAuthor, author_id)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No author with this id: {author_id} found')

    return add_item(db_session=db_session, item_data=book_data, db_model=DBBook)
