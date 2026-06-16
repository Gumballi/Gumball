from sqlalchemy import Column, String, select, delete
from . import BASE
import THANOSPRO.sql as sql

class GMute(BASE):
    __tablename__ = "gmute"
    sender = Column(String(14), primary_key=True)
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, sender, chat_id):
        self.sender = str(sender)
        self.chat_id = str(chat_id)

# Table creation is handled in init_db()

def is_gmuted(sender, chat_id):
    if sql.SESSION is None: return False
    try:
        stmt = select(GMute).where(GMute.sender == str(sender), GMute.chat_id == str(chat_id))
        user = sql.SESSION.execute(stmt).scalars().first()
        return user is not None
    except Exception:
        return False
    finally:
        sql.SESSION.remove()

def gmute(sender, chat_id):
    if sql.SESSION is None: return
    try:
        if not is_gmuted(sender, chat_id):
            adder = GMute(str(sender), str(chat_id))
            sql.SESSION.add(adder)
            sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()

def ungmute(sender, chat_id):
    if sql.SESSION is None: return
    try:
        stmt = delete(GMute).where(GMute.sender == str(sender), GMute.chat_id == str(chat_id))
        sql.SESSION.execute(stmt)
        sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()
