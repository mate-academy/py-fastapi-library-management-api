from database import Base, engine
import models  # Registers Author and Book with Base.metadata

Base.metadata.create_all(bind=engine)
