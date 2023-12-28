from functools import wraps

import sqlalchemy
from fastapi import HTTPException, status


def unique_constraint_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Unique constraint violation. "
                "The resource already exists.",
            )

    return wrapper
