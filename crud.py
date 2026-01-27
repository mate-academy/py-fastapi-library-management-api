from sqlalchemy import select
from sqlalchemy.orm import Session

import models


def get_all_authors(db: Session):
    return db.scalars(select(models.Author)).all()