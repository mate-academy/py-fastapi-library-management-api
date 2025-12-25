from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from models import base

engine = create_engine(
    url="sqlite:///sqlite3",
    echo=True
)

make_session = sessionmaker(
    bind=engine,
    autoflush=False,
)

def get_session():
    base.metadata.drop_all(bind=engine)
    base.metadata.create_all(bind=engine)

    with make_session() as session:
        yield session
