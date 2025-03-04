from sqlalchemy.orm import Session
from fastapi import HTTPException

import crud_utility
import models


def get_list(
        db_session: Session,
        model: type[models.Base],
        skip: int = 0,
        limit: int = 100
) -> list[type[models.Base]]:
    db_query = db_session.query(model)

    if skip is not None:
        db_query = db_query.offset(skip)

    if limit is not None:
        db_query = db_query.limit(limit)

    return db_query.all()


def create(
        db_session: Session,
        item: crud_utility.GSchema
) -> None:
    crud_utility.test_uniqueness(db_session, schema=item)
    crud_utility.add_and_commit(db_session, item)


def get_by_id(
        db_session: Session,
        model: type[models.Base],
        item_id: int
) -> type[models.Base]:
    result: type[models.Base] = (
        db_session
        .query(model)
        .filter(model.id == item_id)
        .first()
    )

    if result is None:
        detail = f"{model.__name__} with {item_id} id not found"
        raise HTTPException(status_code=404, detail=detail)

    return result


def get_books_by_author_id(
        db_session: Session,
        author_id: int,
) -> list[type[models.Book]]:
    result = (
        db_session
        .query(models.Book)
        .filter(models.Book.author_id == author_id)
        .all()
    )

    if not result:
        detail = f"{models.Book.__name__}s with {author_id} id not found"
        raise HTTPException(status_code=404, detail=detail)

    return result
