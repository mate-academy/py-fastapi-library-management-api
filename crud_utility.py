from typing import TypeVar

import schemas
from fastapi import HTTPException
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session


GSchema = TypeVar('GSchema', bound=schemas.BaseModel)


def test_uniqueness(
        db_session: Session,
        schema: GSchema,
) -> None:
    model = schema._model_class
    unique_fields = [
        column.name
        for column in inspect(model).columns
        if column.unique
    ]

    for field in unique_fields:
        # noinspection PyTypeChecker
        result = (
            db_session
            .query(model)
            .filter(getattr(model, field) == getattr(schema, field))
            .first()
        )
        if result:
            raise HTTPException(
                status_code=400,
                detail=f"{model.__name__} with {field} "
                       f'[{getattr(schema, field)}] already exists'
            )


def add_and_commit(db_session: Session, schema: GSchema):
    instance = schema._model_class(**schema.model_dump())
    db_session.add(instance)
    db_session.commit()
