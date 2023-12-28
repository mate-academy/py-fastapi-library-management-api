import json
from datetime import datetime

from database import SessionLocal
from models import Author, Book


def load_data():
    with open("data_db.json", "r") as json_file:
        data = json.load(json_file)

        with SessionLocal() as session:
            for item in data:
                author_data = item.get("author")
                book_data = item.get("book")

                book_data["publication_date"] = datetime.strptime(
                    book_data["publication_date"], "%Y-%m-%d").date()

                author = Author(**author_data)
                book = Book(**book_data, author=author)

                session.add(author)
                session.add(book)

            session.commit()


if __name__ == "__main__":
    load_data()
