from datetime import date
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import crud
import schemas

# Тестові дані
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
    """Очистити базу даних (тільки для тестування)"""
    db = SessionLocal()
    try:
        # Видалити всі книги
        db.query(models.Book).delete()
        # Видалити всіх авторів
        db.query(models.Author).delete()
        db.commit()
        print("🗑️  Базу даних очищено")
    except Exception as e:
        db.rollback()
        print(f"❌ Помилка при очищенні бази: {e}")
    finally:
        db.close()


def seed_database():
    """Наповнити базу даних тестовими даними"""
    print("=" * 60)
    print("НАПОВНЕННЯ БАЗИ ДАНИХ ТЕСТОВИМИ ДАНИМИ")
    print("=" * 60)

    # Запитуємо користувача
    response = input("Очистити існуючі дані? (y/n): ")
    if response.lower() == 'y':
        clear_database()

    db = SessionLocal()

    try:
        # Створюємо авторів
        print("\n📝 СТВОРЕННЯ АВТОРІВ:")
        created_authors = {}

        for author_data in test_authors:
            try:
                # Перевіряємо чи автор вже існує
                existing_author = db.query(models.Author).filter(
                    models.Author.name == author_data["name"]
                ).first()

                if existing_author:
                    print(f"   ⚠️  Автор '{author_data['name']}' вже існує")
                    created_authors[author_data["name"]] = existing_author
                else:
                    author_schema = schemas.AuthorCreate(**author_data)
                    db_author = crud.create_author(db, author_schema)
                    created_authors[author_data["name"]] = db_author
                    print(f"   ✅ Створено автора: {db_author.name}")

            except Exception as e:
                print(f"   ❌ Помилка: {str(e)}")

        # Створюємо книги
        print("\n📚 СТВОРЕННЯ КНИГ:")

        for book_data in test_books:
            try:
                author = created_authors.get(book_data["author_name"])
                if not author:
                    print(f"   ❌ Автор '{book_data['author_name']}' не знайдений")
                    continue

                # Перевіряємо чи книга вже існує
                existing_book = db.query(models.Book).filter(
                    models.Book.title == book_data["title"]
                ).first()

                if existing_book:
                    print(f"   ⚠️  Книга '{book_data['title']}' вже існує")
                else:
                    book_schema = schemas.BookCreate(
                        title=book_data["title"],
                        summary=book_data["summary"],
                        publication_date=book_data["publication_date"],
                        author_id=author.id
                    )
                    db_book = crud.create_book(db, book_schema)
                    print(f"   ✅ Створено книгу: '{db_book.title}'")

            except Exception as e:
                print(f"   ❌ Помилка: {str(e)}")

        # Перевіряємо результати
        author_count = db.query(models.Author).count()
        book_count = db.query(models.Book).count()

        print("\n" + "=" * 60)
        print("РЕЗУЛЬТАТ:")
        print(f"   Авторів: {author_count}")
        print(f"   Книг: {book_count}")
        print("=" * 60)

        print("\n✨ Дані успішно додані до бази!")

    except Exception as e:
        print(f"\n❌ КРИТИЧНА ПОМИЛКА: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
