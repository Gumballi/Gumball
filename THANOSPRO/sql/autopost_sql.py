import threading
from sqlalchemy import Column, String, select, delete
from . import BASE
import THANOSPRO.sql as sql

class Post(BASE):
    __tablename__ = "post"
    target_chat_id = Column(String(14), primary_key=True)
    to_post_chat_id = Column(String(14), primary_key=True, nullable=False)

    def __init__(self, target_chat_id, to_post_chat_id):
        self.to_post_chat_id = str(to_post_chat_id)
        self.target_chat_id = str(target_chat_id)

    def __repr__(self):
        return "<Auto post filter '%s' for %s>" % (self.target_chat_id, self.to_post_chat_id)

# Table creation is handled in init_db()

POST_FILTER_INSERTION_LOCK = threading.RLock()
CHAT_POSTS = {}

def add_post(target_chat_id: str, to_post_chat_id: str):
    if sql.SESSION is None: return
    with POST_FILTER_INSERTION_LOCK:
        try:
            blacklist_filt = Post(str(target_chat_id), str(to_post_chat_id))
            sql.SESSION.merge(blacklist_filt)
            sql.SESSION.commit()
            CHAT_POSTS.setdefault(str(target_chat_id), set()).add(str(to_post_chat_id))
        except Exception:
            sql.SESSION.rollback()
        finally:
            sql.SESSION.remove()

def get_all_post(target_chat_id: str):
    return CHAT_POSTS.get(str(target_chat_id), set())

def is_post(target_chat_id, to_post_chat_id):
    if sql.SESSION is None: return False
    with POST_FILTER_INSERTION_LOCK:
        try:
            stmt = select(Post).where(Post.target_chat_id == str(target_chat_id), Post.to_post_chat_id == str(to_post_chat_id))
            broadcast_group = sql.SESSION.execute(stmt).scalars().first()
            return bool(broadcast_group)
        except Exception:
            return False
        finally:
            sql.SESSION.remove()

def remove_post(target_chat_id, to_post_chat_id):
    if sql.SESSION is None: return False
    with POST_FILTER_INSERTION_LOCK:
        try:
            stmt = delete(Post).where(Post.target_chat_id == str(target_chat_id), Post.to_post_chat_id == str(to_post_chat_id))
            res = sql.SESSION.execute(stmt)
            sql.SESSION.commit()
            if res.rowcount > 0:
                if str(to_post_chat_id) in CHAT_POSTS.get(str(target_chat_id), set()):
                    CHAT_POSTS.get(str(target_chat_id), set()).remove(str(to_post_chat_id))
                return True
            return False
        except Exception:
            sql.SESSION.rollback()
            return False
        finally:
            sql.SESSION.remove()

def load_chat_channels():
    global CHAT_POSTS
    if sql.SESSION is None: return {}
    try:
        stmt = select(Post)
        all_filters = sql.SESSION.execute(stmt).scalars().all()
        CHAT_POSTS = {}
        for x in all_filters:
            CHAT_POSTS.setdefault(x.target_chat_id, set()).add(x.to_post_chat_id)
    except Exception:
        CHAT_POSTS = {}
    finally:
        sql.SESSION.remove()
    return CHAT_POSTS
