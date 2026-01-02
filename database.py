from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Вказуємо посилання на нашу БД
SQLALCHEMY_DATABASE_URI = "sqlite:///library.db"
# Створюємо рушій на якому буде працювати наш застосунок
engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
# Сесії необхідні для роботи з БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Базовий клас як в django models.Model
Base = declarative_base()