from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from database.models import AuthorDB
from schemas import AuthorCreate, AuthorUpdate


def create_author(db: Session, author: AuthorCreate):
    db_author = AuthorDB(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def read_all_authors(db: Session):
    return db.query(AuthorDB).all()


def update_author(db: Session, author_id: int, author: AuthorUpdate):
    db_author = db.query(AuthorDB).filter(AuthorDB.id == author_id).first()

    if db_author:
        print("here ---", author.model_dump())
        for key, value in author.model_dump().items():
            setattr(db_author, key, value)
        db.commit()
        db.refresh(db_author)
        return db_author
    else:
        raise NoResultFound("Author not found")


def delete_author(db: Session, author_id: int):
    db_author = db.query(AuthorDB).filter(AuthorDB.id == author_id).first()

    if db_author:
        db.delete(db_author)
        db.commit()
        return {"message": "Author deleted successfully"}
    else:
        raise NoResultFound("Author not found")


def get_author_by_name(db: Session, name: str):
    return db.query(AuthorDB).filter(AuthorDB.name == name).first()
