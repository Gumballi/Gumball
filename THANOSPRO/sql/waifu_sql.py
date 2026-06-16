from sqlalchemy import Column, String, select, delete
from . import BASE
import THANOSPRO.sql as sql

class Harem(BASE):
    __tablename__ = "harem"
    chat_id = Column(String(14), primary_key=True)
    
    def __init__(self, chat_id):
        self.chat_id = chat_id

# Table creation is handled in init_db()

def add_grp(chat_id: str):
    if sql.SESSION is None: return
    try:
        if not is_harem(chat_id):
            waifu = Harem(str(chat_id))
            sql.SESSION.add(waifu)
            sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()

def rm_grp(chat_id: str):
    if sql.SESSION is None: return
    try:
        stmt = delete(Harem).where(Harem.chat_id == str(chat_id))
        sql.SESSION.execute(stmt)
        sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()

def get_all_grp():
    if sql.SESSION is None: return []
    try:
        stmt = select(Harem)
        return sql.SESSION.execute(stmt).scalars().all()
    except Exception:
        return []
    finally:
        sql.SESSION.remove()

def is_harem(chat_id: str):
    if sql.SESSION is None: return None
    try:
        stmt = select(Harem).where(Harem.chat_id == str(chat_id))
        waifu = sql.SESSION.execute(stmt).scalars().first()
        if waifu:
            return str(waifu.chat_id)
        return None
    except Exception:
        return None
    finally:
        sql.SESSION.remove()
