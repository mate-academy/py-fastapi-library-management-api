from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL бази даних SQLite
# sqlite:/// - протокол для SQLite
# ./library.db - файл бази даних в поточній директорії
SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"

# Створення engine (движка БД)
# Engine керує підключенням до бази даних
# check_same_thread=False - дозволяє SQLite працювати в багатопотоковому середовищі FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Створення SessionLocal - це фабрика для створення сесій БД
# autocommit=False - зміни не зберігаються автоматично (потрібен commit)
# autoflush=False - запити не виконуються автоматично
# bind=engine - прив'язка до нашого engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base - базовий клас для всіх моделей
# Всі моделі в models.py будуть наслідуватися від Base
# Це дозволяє SQLAlchemy автоматично створювати таблиці
Base = declarative_base()


# Dependency функція для отримання сесії БД
# Використовується в FastAPI endpoints як dependency
def get_db():
    """
    Генератор, який створює та закриває сесію БД.
    Використовується як dependency в FastAPI endpoints.
    """
    db = SessionLocal()
    try:
        yield db  # Повертає сесію для використання
    finally:
        db.close()  # Гарантує закриття сесії навіть при помилці

