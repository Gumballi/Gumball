from . import BASE
import THANOSPRO.sql as sql
from sqlalchemy import Column, String, select, delete


class Sudo(BASE):
    __tablename__ = "sudo"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


# Table creation is handled in init_db()


def in_sudo(chat_id):
    if sql.SESSION is None: return None
    try:
        stmt = select(Sudo).where(Sudo.chat_id == str(chat_id))
        return sql.SESSION.execute(stmt).scalars().one()
    except Exception:
        return None
    finally:
        sql.SESSION.remove()


def add_sudo(chat_id):
    if sql.SESSION is None: return
    try:
        adder = Sudo(str(chat_id))
        sql.SESSION.add(adder)
        sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()


def rem_sudo(chat_id):
    if sql.SESSION is None: return
    try:
        stmt = delete(Sudo).where(Sudo.chat_id == str(chat_id))
        sql.SESSION.execute(stmt)
        sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()


def all_sudo():
    if sql.SESSION is None: return 1234
    try:
        stmt = select(Sudo)
        rem = sql.SESSION.execute(stmt).scalars().all()
        if rem:
            return rem
        else:
            return 1234
    except Exception:
        return 1234
    finally:
        sql.SESSION.remove()
