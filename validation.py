from fastapi import HTTPException
from sqlalchemy.orm import Session

import crud


def validate_author_with_name_exists(
        db: Session,
        author_name: str,
        author_id: int | None = None,
):
    db_author = crud.get_author_by_name(db=db, name=author_name)
    if db_author and db_author.id != author_id:
        raise HTTPException(
            status_code=400,
            detail=f"Author with name {author_name} already exists"
        )
