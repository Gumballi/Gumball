from sqlalchemy import Column, String, select, delete
from . import BASE
import THANOSPRO.sql as sql

class Husbando(BASE):
    __tablename__ = "husbando"
    chat_id = Column(String(14), primary_key=True)
    
    def __init__(self, chat_id):
        self.chat_id = chat_id

# Table creation is handled in init_db()

def add_hus_grp(chat_id: str):
    if sql.SESSION is None: return
    try:
        if not is_husb(chat_id):
            husba = Husbando(str(chat_id))
            sql.SESSION.add(husba)
            sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()

def rm_hus_grp(chat_id: str):
    if sql.SESSION is None: return
    try:
        stmt = delete(Husbando).where(Husbando.chat_id == str(chat_id))
        sql.SESSION.execute(stmt)
        sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()

def get_all_hus_grp():
    if sql.SESSION is None: return []
    try:
        stmt = select(Husbando)
        return sql.SESSION.execute(stmt).scalars().all()
    except Exception:
        return []
    finally:
        sql.SESSION.remove()

def is_husb(chat_id: str):
    if sql.SESSION is None: return None
    try:
        stmt = select(Husbando).where(Husbando.chat_id == str(chat_id))
        husba = sql.SESSION.execute(stmt).scalars().first()
        if husba:
            return str(husba.chat_id)
        return None
    except Exception:
        return None
    finally:
        sql.SESSION.remove()
