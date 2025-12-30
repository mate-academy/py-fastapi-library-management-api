from datetime import date
from database import SessionLocal
import models
import crud
import schemas

# Test data
test_authors = [
    {
        "name": "George Orwell",
        "bio": "English novelist, essayist, journalist, and critic. His work is characterised by lucid prose, biting social criticism, opposition to totalitarianism, and outspoken support of democratic socialism."
    },
    {
        "name": "J.K. Rowling",
        "bio": "British author, best known for writing the Harry Potter fantasy series. The books have won multiple awards and sold more than 500 million copies, becoming the best-selling book series in history."
    },
    {
        "name": "Stephen King",
        "bio": "American author of horror, supernatural fiction, suspense, crime, science-fiction, and fantasy novels. Described as the 'King of Horror', his books have sold more than 350 million copies."
    },
    {
        "name": "Agatha Christie",
        "bio": "English writer known for her 66 detective novels and 14 short story collections, particularly those revolving around fictional detectives Hercule Poirot and Miss Marple."
    }
]

test_books = [
    {
        "title": "1984",
        "summary": "A dystopian social science fiction novel and cautionary tale about the dangers of totalitarianism.",
        "publication_date": date(1949, 6, 8),
        "author_name": "George Orwell"
    },
    {
        "title": "Harry Potter and the Philosopher's Stone",
        "summary": "The first novel in the Harry Potter series.",
        "publication_date": date(1997, 6, 26),
        "author_name": "J.K. Rowling"
    },
    {
        "title": "The Shining",
        "summary": "A horror novel about a family's winter stay at an isolated hotel.",
        "publication_date": date(1977, 1, 28),
        "author_name": "Stephen King"
    },
    {
        "title": "Murder on the Orient Express",
        "summary": "A detective novel featuring the Belgian detective Hercule Poirot.",
        "publication_date": date(1934, 1, 1),
        "author_name": "Agatha Christie"
    }
]


def clear_database():
    """Clear db (Only for testing)"""
    db = SessionLocal()
    try:
        # Delete all books
        db.query(models.Book).delete()
        # Delete all authors
        db.query(models.Author).delete()
        db.commit()
        print("🗑️  database cleared!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error while clearing the database: {e}")
    finally:
        db.close()


def seed_database():
    """Fill the database with test data"""
    print("=" * 60)
    print("FILL THE DATABASE WITH TEST DATA")
    print("=" * 60)

    # User request
    response = input("Clear existing data? (y/n): ")
    if response.lower() == 'y':
        clear_database()

    db = SessionLocal()

    try:
        # Create authors
        print("\n📝 Creating authors:")
        created_authors = {}

        for author_data in test_authors:
            try:
                # Checking if the author already exists
                existing_author = db.query(models.Author).filter(
                    models.Author.name == author_data["name"]
                ).first()

                if existing_author:
                    print(f"   ⚠️  Author '{author_data['name']}' is already existing.")
                    created_authors[author_data["name"]] = existing_author
                else:
                    author_schema = schemas.AuthorCreate(**author_data)
                    db_author = crud.create_author(db, author_schema)
                    created_authors[author_data["name"]] = db_author
                    print(f"   ✅ The author has been created: {db_author.name}")

            except Exception as e:
                print(f"   ❌ Error: {str(e)}")

        # Створюємо книги
        print("\n📚 Creating books:")

        for book_data in test_books:
            try:
                author = created_authors.get(book_data["author_name"])
                if not author:
                    print(f"   ❌ Author '{book_data['author_name']}' not found.")
                    continue

                # Checking if the book is already exist
                existing_book = db.query(models.Book).filter(
                    models.Book.title == book_data["title"]
                ).first()

                if existing_book:
                    print(f"   ⚠️  Book '{book_data['title']}' is already existing")
                else:
                    book_schema = schemas.BookCreate(
                        title=book_data["title"],
                        summary=book_data["summary"],
                        publication_date=book_data["publication_date"],
                        author_id=author.id
                    )
                    db_book = crud.create_book(db, book_schema)
                    print(f"   ✅ The book has been created: '{db_book.title}'")

            except Exception as e:
                print(f"   ❌ Error: {str(e)}")

        # Checking results
        author_count = db.query(models.Author).count()
        book_count = db.query(models.Book).count()

        print("\n" + "=" * 60)
        print("Result:")
        print(f"   Authors: {author_count}")
        print(f"   Books: {book_count}")
        print("=" * 60)

        print("\n✨ Data successfully added to the database!")

    except Exception as e:
        print(f"\n❌ Critical Error: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
