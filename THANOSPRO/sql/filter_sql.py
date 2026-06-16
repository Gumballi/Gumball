from sqlalchemy import Column, LargeBinary, Numeric, String, UnicodeText, select, delete
from . import BASE
import THANOSPRO.sql as sql

class Filters(BASE):
    __tablename__ = "filters"
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True)
    reply = Column(UnicodeText)
    snip_type = Column(Numeric)
    media_id = Column(UnicodeText)
    media_access_hash = Column(UnicodeText)
    media_file_reference = Column(LargeBinary)

    def __init__(self, chat_id, keyword, reply, snip_type, media_id=None, media_access_hash=None, media_file_reference=None):
        self.chat_id = chat_id
        self.keyword = keyword
        self.reply = reply
        self.snip_type = snip_type
        self.media_id = media_id
        self.media_access_hash = media_access_hash
        self.media_file_reference = media_file_reference

# Table creation is handled in init_db()

def get_filter(chat_id, keyword):
    if sql.SESSION is None: return None
    try:
        stmt = select(Filters).where(Filters.chat_id == str(chat_id), Filters.keyword == keyword)
        return sql.SESSION.execute(stmt).scalars().first()
    except Exception:
        return None
    finally:
        sql.SESSION.remove()

def get_all_filters(chat_id):
    if sql.SESSION is None: return []
    try:
        stmt = select(Filters).where(Filters.chat_id == str(chat_id))
        return sql.SESSION.execute(stmt).scalars().all()
    except Exception:
        return []
    finally:
        sql.SESSION.remove()

def add_filter(chat_id, keyword, reply, snip_type, media_id, media_access_hash, media_file_reference):
    if sql.SESSION is None: return
    try:
        stmt = select(Filters).where(Filters.chat_id == str(chat_id), Filters.keyword == keyword)
        adder = sql.SESSION.execute(stmt).scalars().first()
        if adder:
            adder.reply = reply
            adder.snip_type = snip_type
            adder.media_id = media_id
            adder.media_access_hash = media_access_hash
            adder.media_file_reference = media_file_reference
        else:
            adder = Filters(chat_id, keyword, reply, snip_type, media_id, media_access_hash, media_file_reference)
            sql.SESSION.add(adder)
        sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()

def remove_filter(chat_id, keyword):
    if sql.SESSION is None: return
    try:
        stmt = delete(Filters).where(Filters.chat_id == str(chat_id), Filters.keyword == keyword)
        sql.SESSION.execute(stmt)
        sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()

def remove_all_filters(chat_id):
    if sql.SESSION is None: return
    try:
        stmt = delete(Filters).where(Filters.chat_id == str(chat_id))
        sql.SESSION.execute(stmt)
        sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()
