from sqlalchemy import Column, String, select, delete
from . import BASE
import THANOSPRO.sql as sql

class ECHOSQL(BASE):
    __tablename__ = "echo_sql"
    user_id = Column(String(14), primary_key=True)
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, user_id, chat_id):
        self.user_id = str(user_id)
        self.chat_id = str(chat_id)

# Table creation is handled in init_db()

def is_echo(user_id, chat_id):
    if sql.SESSION is None: return None
    try:
        stmt = select(ECHOSQL).where(ECHOSQL.user_id == str(user_id), ECHOSQL.chat_id == str(chat_id))
        return sql.SESSION.execute(stmt).scalars().first()
    except Exception:
        return None
    finally:
        sql.SESSION.remove()

def get_all_echos():
    if sql.SESSION is None: return []
    try:
        stmt = select(ECHOSQL)
        return sql.SESSION.execute(stmt).scalars().all()
    except Exception:
        return []
    finally:
        sql.SESSION.remove()

def addecho(user_id, chat_id):
    if sql.SESSION is None: return
    try:
        if not is_echo(user_id, chat_id):
            adder = ECHOSQL(str(user_id), str(chat_id))
            sql.SESSION.add(adder)
            sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()

def remove_echo(user_id, chat_id):
    if sql.SESSION is None: return
    try:
        stmt = delete(ECHOSQL).where(ECHOSQL.user_id == str(user_id), ECHOSQL.chat_id == str(chat_id))
        sql.SESSION.execute(stmt)
        sql.SESSION.commit()
    except Exception:
        sql.SESSION.rollback()
    finally:
        sql.SESSION.remove()
