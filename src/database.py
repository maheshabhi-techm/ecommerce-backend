from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .security import config

engine = create_engine(config.settings.database_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
