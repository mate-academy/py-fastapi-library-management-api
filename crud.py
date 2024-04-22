from sqlalchemy.orm import Session
from db.models import DbAuthor, DbBook
from schemas import AuthorCreate, BookCreate


def get_author_list(db: Session) -> list[DbAuthor]:
    return db.query(DbAuthor).all()


def get_author_detail(db: Session, author_id: int) -> DbAuthor:
    return db.query(DbAuthor).get(author_id)


def get_author_by_name(db: Session, name: str) -> DbAuthor:
    return (
        db.query(DbAuthor).filter(DbAuthor.name == name).first()
    )


def create_author(db: Session, author: AuthorCreate) -> DbAuthor:
    db_author = DbAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_book_list(
    db: Session,
    author_id: int | None = None,
    author_name: str | None = None,
    skip: int = 0,
    limit: int = 10
) -> list[DbBook]:
    queryset = db.query(DbBook)

    if author_id is not None:
        queryset = queryset.filter(
            DbBook.author_id == author_id
        )

    if author_name is not None:
        queryset = queryset.join(DbBook.author).filter(
            DbAuthor.name.ilike(f"%{author_name}%")
        )

    queryset = queryset.offset(skip).limit(limit)

    return queryset.all()


def get_book_detail(db: Session, book_id: int) -> DbBook:
    return db.query(DbBook).get(book_id)


def create_book(db: Session, book: BookCreate) -> DbBook:
    db_book = DbBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
