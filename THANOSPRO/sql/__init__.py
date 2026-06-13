import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from THANOSPRO.config import Config

# DB_URI = os.environ.get("DATABASE_URL")


def start() -> scoped_session:
    db_uri = Config.DB_URI
    if db_uri and db_uri.startswith("postgres://"):
        db_uri = db_uri.replace("postgres://", "postgresql://", 1)
    
    if not db_uri or db_uri == "Your value":
        raise AttributeError("DB_URI is not configured.")

    engine = create_engine(db_uri)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


try:
    BASE = declarative_base()
    SESSION = start()
except AttributeError as e:
    # this is a dirty way for the work-around required for #23
    print(
        "DB_URI is not configured. Features depending on the database might have issues."
    )
    print(str(e))
