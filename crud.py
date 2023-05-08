from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session):
    return db.query(models.Author).all()


def create_author(db: Session, author: schemas.Author):
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_detail_author(db: Session, author_id: int):
    return (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )


def update_author(db: Session, author_id: int, author: schemas.AuthorUpdate):
    author_to_update = get_detail_author(db, author_id)
    if not author_to_update:
        return None
    for key, value in author.dict().items():
        setattr(author_to_update, key, value)
    db.commit()
    db.refresh(author_to_update)
    return author_to_update


def delete_author(db: Session, author_id: int):
    author_to_delete = get_detail_author(db, author_id)
    if not author_to_delete:
        return None
    db.delete(author_to_delete)
    db.commit()
    return author_to_delete

