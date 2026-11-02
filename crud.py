import models


def create_author(db, author):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(db, skip=0, limit=10):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author(db, author_id):
    return (
        db.query(models.Author)
        .filter(models.Author.id == author_id)
        .first()
    )


def create_book(db, book, author_id):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db, skip=0, limit=10, author_id=None):
    query = db.query(models.Book)
    if author_id:
        query = query.filter(models.Book.author_id == author_id)
    return query.offset(skip).limit(limit).all()
