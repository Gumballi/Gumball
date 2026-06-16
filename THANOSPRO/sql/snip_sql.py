from sqlalchemy import Column, Numeric, UnicodeText, select, delete
from . import BASE
import THANOSPRO.sql as sql

class Note(BASE):
    __tablename__ = "snip"
    keyword = Column(UnicodeText, primary_key=True, nullable=False)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Numeric)

    def __init__(self, keyword, reply, f_mesg_id):
        self.keyword = keyword
        self.reply = reply
        self.f_mesg_id = f_mesg_id

# Table creation is handled in init_db()

def get_note(keyword):
    if sql.SESSION is None: return None
    try:
        stmt = select(Note).where(Note.keyword == keyword)
        return sql.SESSION.execute(stmt).scalars().first()
    except Exception:
        return None
    finally:
        sql.SESSION.remove()

def get_notes():
    if sql.SESSION is None: return []
    try:
        stmt = select(Note)
        return sql.SESSION.execute(stmt).scalars().all()
    except Exception:
        return []
    finally:
        sql.SESSION.remove()

def add_note(keyword, reply, f_mesg_id):
    if sql.SESSION is None: return False
    try:
        to_check = get_note(keyword)
        if not to_check:
            adder = Note(keyword, reply, f_mesg_id)
            sql.SESSION.add(adder)
            sql.SESSION.commit()
            return True
        
        stmt = delete(Note).where(Note.keyword == keyword)
        sql.SESSION.execute(stmt)
        adder = Note(keyword, reply, f_mesg_id)
        sql.SESSION.add(adder)
        sql.SESSION.commit()
        return False
    except Exception:
        sql.SESSION.rollback()
        return False
    finally:
        sql.SESSION.remove()

def rm_note(keyword):
    if sql.SESSION is None: return False
    try:
        stmt = delete(Note).where(Note.keyword == keyword)
        res = sql.SESSION.execute(stmt)
        sql.SESSION.commit()
        return res.rowcount > 0
    except Exception:
        sql.SESSION.rollback()
        return False
    finally:
        sql.SESSION.remove()
