from sqlalchemy.orm import Session

import models
import schemas


def get_author_list(db: Session):
    return db.query(models.Author).all()


def create_author(author: schemas.AuthorCreate, db: Session):
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )

    db.add(db_author)
    print("add===========================")
    db.commit()
    print("commit===========================")
    db.refresh(db_author)
    print("refresh===========================")

    return db_author
