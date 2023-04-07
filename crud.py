from sqlalchemy.orm import Session

from library import models
import schemas


def get_all_authors(library: Session):
    return library.query(models.Author).all()


def create_author(library: Session, author: schemas.AuthorCreate):
    library_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    library.add(library_author)
    library.commit()
    library.refresh(library_author)

    return library_author
