from sqlalchemy import Column, String, select, delete
from . import BASE
import THANOSPRO.sql as sql

class PMPermit(BASE):
    __tablename__ = "pmpermit"
    chat_id = Column(String(14), primary_key=True)
    reason = Column(String(127))

    def __init__(self, chat_id, reason=""):
        self.chat_id = chat_id
        self.reason = reason

# Table creation is handled in init_db()

def is_approved(chat_id):
    if sql.SESSION is None: return None
    try:
        stmt = select(PMPermit).where(PMPermit.chat_id == str(chat_id))
        return sql.SESSION.execute(stmt).scalars().first()
    except Exception:
        return None
    finally:
        sql.SESSION.remove()

def approve(chat_id, reason):
    if sql.SESSION is None: return
    try:
        if not is_approved(chat_id):
            adder = PMPermit(str(chat_id), str(reason))
            sql.SESSION.add(adder)
            sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()

def disapprove(chat_id):
    if sql.SESSION is None: return
    try:
        stmt = delete(PMPermit).where(PMPermit.chat_id == str(chat_id))
        sql.SESSION.execute(stmt)
        sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()

def get_all_approved():
    if sql.SESSION is None: return []
    try:
        stmt = select(PMPermit)
        return sql.SESSION.execute(stmt).scalars().all()
    except Exception:
        return []
    finally:
        sql.SESSION.remove()
