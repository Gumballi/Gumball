from sqlalchemy import Column, String, Numeric, select, delete
from . import BASE
import THANOSPRO.sql as sql

class forceSubscribe(BASE):
    __tablename__ = "forceSubscribe"
    chat_id = Column(Numeric, primary_key=True)
    channel = Column(String)

    def __init__(self, chat_id, channel):
        self.chat_id = chat_id
        self.channel = channel

# Table creation is handled in init_db()

def is_fsub(chat_id):
    if sql.SESSION is None: return None
    try:
        stmt = select(forceSubscribe).where(forceSubscribe.chat_id == chat_id)
        return sql.SESSION.execute(stmt).scalars().first()
    except Exception:
        return None
    finally:
        sql.SESSION.remove()

def add_fsub(chat_id, channel):
    if sql.SESSION is None: return
    try:
        stmt = select(forceSubscribe).where(forceSubscribe.chat_id == chat_id)
        adder = sql.SESSION.execute(stmt).scalars().first()
        if adder:
            adder.channel = channel
        else:
            adder = forceSubscribe(chat_id, channel)
            sql.SESSION.add(adder)
        sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()

def rm_fsub(chat_id):
    if sql.SESSION is None: return
    try:
        stmt = delete(forceSubscribe).where(forceSubscribe.chat_id == chat_id)
        sql.SESSION.execute(stmt)
        sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()

def all_fsub():
    if sql.SESSION is None: return []
    try:
        stmt = select(forceSubscribe)
        return sql.SESSION.execute(stmt).scalars().all()
    except Exception:
        return []
    finally:
        sql.SESSION.remove()
