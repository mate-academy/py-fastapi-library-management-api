from sqlalchemy.orm import declarative_base


Base = declarative_base()

DATABASE_URL = "sqlite+aiosqlite:///./library.db"
