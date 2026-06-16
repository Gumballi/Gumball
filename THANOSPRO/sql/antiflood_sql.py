import threading
from sqlalchemy import Column, Integer, String, select, delete
from . import BASE
import THANOSPRO.sql as sql

DEF_COUNT = 0
DEF_LIMIT = 0
DEF_OBJ = (None, DEF_COUNT, DEF_LIMIT)

class FloodControl(BASE):
    __tablename__ = "antiflood"
    chat_id = Column(String(14), primary_key=True)
    user_id = Column(Integer)
    count = Column(Integer, default=DEF_COUNT)
    limit = Column(Integer, default=DEF_LIMIT)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)

    def __repr__(self):
        return "<flood control for %s>" % self.chat_id

# Table creation is handled in init_db()

INSERTION_LOCK = threading.RLock()
CHAT_FLOOD = {}

def set_flood(chat_id, amount):
    if sql.SESSION is None: return
    with INSERTION_LOCK:
        try:
            stmt = select(FloodControl).where(FloodControl.chat_id == str(chat_id))
            flood = sql.SESSION.execute(stmt).scalars().first()
            if not flood:
                flood = FloodControl(str(chat_id))
                sql.SESSION.add(flood)
            
            flood.user_id = None
            flood.limit = amount
            CHAT_FLOOD[str(chat_id)] = (None, DEF_COUNT, amount)
            sql.SESSION.commit()
        except Exception:
            sql.SESSION.rollback()
        finally:
            sql.SESSION.remove()

def update_flood(chat_id: str, user_id) -> bool:
    if str(chat_id) in CHAT_FLOOD:
        curr_user_id, count, limit = CHAT_FLOOD.get(str(chat_id), DEF_OBJ)
        if limit == 0: return False
        if user_id != curr_user_id or user_id is None:
            CHAT_FLOOD[str(chat_id)] = (user_id, DEF_COUNT + 1, limit)
            return False
        count += 1
        if count > limit:
            CHAT_FLOOD[str(chat_id)] = (None, DEF_COUNT, limit)
            return True
        CHAT_FLOOD[str(chat_id)] = (user_id, count, limit)
        return False

def get_flood_limit(chat_id):
    return CHAT_FLOOD.get(str(chat_id), DEF_OBJ)[2]

def migrate_chat(old_chat_id, new_chat_id):
    if sql.SESSION is None: return
    with INSERTION_LOCK:
        try:
            stmt = select(FloodControl).where(FloodControl.chat_id == str(old_chat_id))
            flood = sql.SESSION.execute(stmt).scalars().first()
            if flood:
                CHAT_FLOOD[str(new_chat_id)] = CHAT_FLOOD.get(str(old_chat_id), DEF_OBJ)
                flood.chat_id = str(new_chat_id)
                sql.SESSION.commit()
        except Exception:
            sql.SESSION.rollback()
        finally:
            sql.SESSION.remove()

def load_flood_settings():
    global CHAT_FLOOD
    if sql.SESSION is None: return {}
    try:
        stmt = select(FloodControl)
        all_chats = sql.SESSION.execute(stmt).scalars().all()
        CHAT_FLOOD = {chat.chat_id: (None, DEF_COUNT, chat.limit) for chat in all_chats}
    except Exception:
        CHAT_FLOOD = {}
    finally:
        sql.SESSION.remove()
    return CHAT_FLOOD
