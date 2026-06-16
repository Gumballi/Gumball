from sqlalchemy import BigInteger, Column, Numeric, String, UnicodeText, select, delete
from . import BASE
import THANOSPRO.sql as sql

class Welcome(BASE):
    __tablename__ = "welcome"
    chat_id = Column(String(14), primary_key=True)
    previous_welcome = Column(BigInteger)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Numeric)

    def __init__(self, chat_id, previous_welcome, reply, f_mesg_id):
        self.chat_id = str(chat_id)
        self.previous_welcome = previous_welcome
        self.reply = reply
        self.f_mesg_id = f_mesg_id

# Table creation is handled in init_db()

def get_welcome(chat_id):
    if sql.SESSION is None: return None
    try:
        stmt = select(Welcome).where(Welcome.chat_id == str(chat_id))
        return sql.SESSION.execute(stmt).scalars().first()
    except Exception:
        return None
    finally:
        sql.SESSION.remove()

def get_current_welcome(chat_id):
    return get_welcome(chat_id)

def add_welcome(chat_id, previous_welcome, reply, f_mesg_id):
    if sql.SESSION is None: return False
    try:
        to_check = get_welcome(chat_id)
        if to_check:
            stmt = delete(Welcome).where(Welcome.chat_id == str(chat_id))
            sql.SESSION.execute(stmt)
            sql.SESSION.commit()
        
        adder = Welcome(chat_id, previous_welcome, reply, f_mesg_id)
        sql.SESSION.add(adder)
        sql.SESSION.commit()
        return not to_check
    except Exception:
        sql.SESSION.rollback()
        return False
    finally:
        sql.SESSION.remove()

def rm_welcome(chat_id):
    if sql.SESSION is None: return False
    try:
        stmt = delete(Welcome).where(Welcome.chat_id == str(chat_id))
        res = sql.SESSION.execute(stmt)
        sql.SESSION.commit()
        return res.rowcount > 0
    except Exception:
        sql.SESSION.rollback()
        return False
    finally:
        sql.SESSION.remove()

def update_welcome(chat_id, previous_welcome):
    if sql.SESSION is None: return
    try:
        stmt = select(Welcome).where(Welcome.chat_id == str(chat_id))
        row = sql.SESSION.execute(stmt).scalars().first()
        if row:
            row.previous_welcome = previous_welcome
            sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()
