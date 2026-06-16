import threading
from sqlalchemy import Column, String, UnicodeText, distinct, func, select, delete
from . import BASE
import THANOSPRO.sql as sql

class BlackListFilters(BASE):
    __tablename__ = "blacklist"
    chat_id = Column(String(14), primary_key=True)
    trigger = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, chat_id, trigger):
        self.chat_id = str(chat_id)
        self.trigger = trigger

    def __repr__(self):
        return "<Blacklist filter '%s' for %s>" % (self.trigger, self.chat_id)

# Table creation is handled in init_db()

BLACKLIST_FILTER_INSERTION_LOCK = threading.RLock()
CHAT_BLACKLISTS = {}

def add_to_blacklist(chat_id, trigger):
    if sql.SESSION is None: return
    with BLACKLIST_FILTER_INSERTION_LOCK:
        try:
            blacklist_filt = BlackListFilters(str(chat_id), trigger)
            sql.SESSION.merge(blacklist_filt)
            sql.SESSION.commit()
            CHAT_BLACKLISTS.setdefault(str(chat_id), set()).add(trigger)
        except Exception:
            sql.SESSION.rollback()
        finally:
            sql.SESSION.remove()

def rm_from_blacklist(chat_id, trigger):
    if sql.SESSION is None: return False
    with BLACKLIST_FILTER_INSERTION_LOCK:
        try:
            stmt = delete(BlackListFilters).where(BlackListFilters.chat_id == str(chat_id), BlackListFilters.trigger == trigger)
            res = sql.SESSION.execute(stmt)
            sql.SESSION.commit()
            if res.rowcount > 0:
                if trigger in CHAT_BLACKLISTS.get(str(chat_id), set()):
                    CHAT_BLACKLISTS.get(str(chat_id), set()).remove(trigger)
                return True
            return False
        except Exception:
            sql.SESSION.rollback()
            return False
        finally:
            sql.SESSION.remove()

def get_chat_blacklist(chat_id):
    return CHAT_BLACKLISTS.get(str(chat_id), set())

def load_chat_blacklists():
    global CHAT_BLACKLISTS
    if sql.SESSION is None: return {}
    try:
        stmt = select(BlackListFilters)
        all_filters = sql.SESSION.execute(stmt).scalars().all()
        CHAT_BLACKLISTS = {}
        for x in all_filters:
            CHAT_BLACKLISTS.setdefault(x.chat_id, set()).add(x.trigger)
    except Exception:
        CHAT_BLACKLISTS = {}
    finally:
        sql.SESSION.remove()
    return CHAT_BLACKLISTS
