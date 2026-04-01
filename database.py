import create_engine from sqlalchemy


sqllite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqllite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)