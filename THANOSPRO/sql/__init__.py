import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from THANOSPRO.config import Config

BASE = declarative_base()
SESSION = None

def init_db(db_uri=None):
    global SESSION
    if not db_uri:
        db_uri = Config.DB_URI
    
    if not db_uri:
        print("DATABASE_URL is not configured. Database features will be disabled.")
        return None

    # Handle deprecated postgres:// scheme
    if db_uri.startswith("postgres://"):
        db_uri = db_uri.replace("postgres://", "postgresql://", 1)

    try:
        engine = create_engine(db_uri)
        BASE.metadata.bind = engine
        BASE.metadata.create_all(engine)
        SESSION = scoped_session(sessionmaker(bind=engine, autoflush=False))
        
        # Load settings into memory after DB init
        from .antiflood_sql import load_flood_settings
        from .blacklist_sql import load_chat_blacklists
        from .autopost_sql import load_chat_channels
        
        load_flood_settings()
        load_chat_blacklists()
        load_chat_channels()
        
        return SESSION
    except Exception as e:
        print(f"Error initializing database: {e}")
        return None

# Placeholder for modules that import SESSION directly
# They should ideally call init_db first
