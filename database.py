from sqlalchemy import create_engine, declarative_base


engine = create_engine("sqlite://app.db")

Base = declarative_base()