import sys
from telethon import TelegramClient
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.sessions import StringSession
from THANOSPRO.config import Config

# Global clients to be populated by the startup function
rishu = None
H2 = None
H3 = None
H4 = None
H5 = None
THANOSPRO_BOT = None

def get_multi_clients():
    return {"H2": H2, "H3": H3, "H4": H4, "H5": H5}

def create_user_client(session_str):
    if not session_str:
        return None
    try:
        return TelegramClient(
            session=StringSession(str(session_str)),
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            connection=ConnectionTcpAbridged,
            auto_reconnect=True,
            connection_retries=None,
        )
    except Exception as e:
        print(f"Error creating user client: {e}")
        return None

def create_bot_client():
    try:
        return TelegramClient(
            session="rishu-TBot",
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            connection=ConnectionTcpAbridged,
            auto_reconnect=True,
            connection_retries=None,
        )
    except Exception as e:
        print(f"Error creating bot client: {e}")
        return None

def init_all_clients():
    global rishu, H2, H3, H4, H5, THANOSPRO_BOT
    
    rishu = create_user_client(Config.THANOSPRO_SESSION)
    if not rishu:
        print("THANOSPRO_SESSION is missing or invalid. Exiting.")
        sys.exit(1)
        
    H2 = create_user_client(Config.SESSION_2)
    H3 = create_user_client(Config.SESSION_3)
    H4 = create_user_client(Config.SESSION_4)
    H5 = create_user_client(Config.SESSION_5)
    
    THANOSPRO_BOT = create_bot_client()
    if not THANOSPRO_BOT:
        print("Bot token or configuration is missing. Exiting.")
        sys.exit(1)
    
    return rishu, THANOSPRO_BOT, get_multi_clients()
