from sqlalchemy import Column, String, select, delete
from . import BASE
import THANOSPRO.sql as sql

class Mute(BASE):
    __tablename__ = "mute"
    sender = Column(String(14), primary_key=True)
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, sender, chat_id):
        self.sender = str(sender)
        self.chat_id = str(chat_id)

# Table creation is handled in init_db()

def is_muted(sender, chat_id):
    if sql.SESSION is None: return False
    try:
        stmt = select(Mute).where(Mute.sender == str(sender), Mute.chat_id == str(chat_id))
        user = sql.SESSION.execute(stmt).scalars().first()
        return user is not None
    except Exception:
        return False
    finally:
        sql.SESSION.remove()

def mute(sender, chat_id):
    if sql.SESSION is None: return
    try:
        if not is_muted(sender, chat_id):
            adder = Mute(str(sender), str(chat_id))
            sql.SESSION.add(adder)
            sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()

def unmute(sender, chat_id):
    if sql.SESSION is None: return
    try:
        stmt = delete(Mute).where(Mute.sender == str(sender), Mute.chat_id == str(chat_id))
        sql.SESSION.execute(stmt)
        sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()

def get_all_muted():
    if sql.SESSION is None: return []
    try:
        stmt = select(Mute)
        return sql.SESSION.execute(stmt).scalars().all()
    except Exception:
        return []
    finally:
        sql.SESSION.remove()
