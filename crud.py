from sqlalchemy.orm import Session

import models


def str_to_int(author_ids: str) -> list[int]:
    return list(map(int, author_ids.split(",")))


def get_books_list(
    db: Session, author_ids: str | None = None
) -> list[models.Book]:
    queryset = db.query(models.Book)

    if author_ids:
        author_ids = str_to_int(author_ids)
        queryset = queryset.filter(models.Book.author_id.in_(author_ids))
    return queryset.all()
