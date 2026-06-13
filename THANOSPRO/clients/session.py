import sys

from telethon import TelegramClient
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.sessions import StringSession

from THANOSPRO.config import Config


def create_client(session_str, name):
    if session_str:
        session = StringSession(str(session_str))
    else:
        session = name
    return TelegramClient(
        session=session,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )

rishu = create_client(Config.THANOSPRO_SESSION, "THANOSPRO")
H2 = create_client(Config.SESSION_2, "H2") if Config.SESSION_2 else None
H3 = create_client(Config.SESSION_3, "H3") if Config.SESSION_3 else None
H4 = create_client(Config.SESSION_4, "H4") if Config.SESSION_4 else None
H5 = create_client(Config.SESSION_5, "H5") if Config.SESSION_5 else None

THANOSPRO = TelegramClient(
    session="rishu-TBot",
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    connection=ConnectionTcpAbridged,
    auto_reconnect=True,
    connection_retries=None,
)
