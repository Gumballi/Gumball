from sqlalchemy import Column, String, select, delete
from . import BASE
import THANOSPRO.sql as sql

class GBan(BASE):
    __tablename__ = "gban"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id

# Table creation is handled in init_db()

def is_gbanned(chat_id):
    if sql.SESSION is None: return None
    try:
        stmt = select(GBan).where(GBan.chat_id == str(chat_id))
        return sql.SESSION.execute(stmt).scalars().first()
    except Exception:
        return None
    finally:
        sql.SESSION.remove()

def gbaner(chat_id):
    if sql.SESSION is None: return
    try:
        if not is_gbanned(chat_id):
            adder = GBan(str(chat_id))
            sql.SESSION.add(adder)
            sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()

def ungbaner(chat_id):
    if sql.SESSION is None: return
    try:
        stmt = delete(GBan).where(GBan.chat_id == str(chat_id))
        sql.SESSION.execute(stmt)
        sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()

def all_gbanned():
    if sql.SESSION is None: return []
    try:
        stmt = select(GBan)
        return sql.SESSION.execute(stmt).scalars().all()
    except Exception:
        return []
    finally:
        sql.SESSION.remove()
