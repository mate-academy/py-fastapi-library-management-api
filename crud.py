from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Author


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(Author).offset(skip).limit(limit)
    result = db.execute(stmt)
    return result.scalars().all()
