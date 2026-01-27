from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session):
    return db.scalars(select(models.Author)).all()

def create_author(db: Session, author_data: schemas.AuthorCreate):
    new_author = models.Author(
        name=author_data.name,
        bio=author_data.bio,
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)

