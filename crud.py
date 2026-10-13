from sqlalchemy.orm import Session
import models
import schemas


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
):
    query = db.query(models.DBBook)
    if author_id is not None:
        query = query.filter(models.DBBook.author_id == author_id)

    return query.offset(skip).limit(limit).all()

def get_author_by_name(db: Session, name: str):
    return (
        db.query(models.DBAuthor)
        .filter(models.DBAuthor.name == name)
        .first()
    )

def create_book(db: Session, book: schemas.BookCreate, author_id: int):
    new_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

def get_book_by_id(db: Session, book_id: int):
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()

def delete_book(db: Session, book_id: int):
    db.query(models.DBBook).filter(models.DBBook.id == book_id).delete()
    db.commit()

def update_book(db:Session, book_id: int, book: schemas.BookUpdate):
    db_book = get_book_by_id(db, book_id)
    if db_book is None:
        return None

    for field, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)

    return db_book

def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()

def create_author(db: Session, author: schemas.AuthorCreate):
    new_author = models.DBAuthor(name=author.name, bio=author.bio)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author

def get_author_by_id(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()

def delete_author(db: Session, author_id: int):
    db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).delete()
    db.commit()

def update_author(db:Session, author_id: int, author: schemas.AuthorUpdate):
    db_author = get_author_by_id(db, author_id)

    if db_author is None:
        return None

    for field, value in author.model_dump(exclude_unset=True).items():
        setattr(db_author, field, value)

    db.commit()
    db.refresh(db_author)
    return db_author