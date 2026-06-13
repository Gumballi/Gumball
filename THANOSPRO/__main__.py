import glob
import asyncio
import os
import sys
import datetime
import random
import time
from . import *
from pathlib import Path
from telethon import Button, TelegramClient
from telethon.utils import get_peer_id
from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot

from THANOSPRO import LOGS, bot, tbot
from THANOSPRO.clients.session import rishu, H2, H3, H4, H5
from THANOSPRO.config import Config
from THANOSPRO.utils import join_it, load_module, logger_check, start_msg, update_sudo, plug_channel
from THANOSPRO.version import __rishu__ as rishuver
from telethon.sessions import StringSession
from telethon.sync import TelegramClient
hl = Config.HANDLER

rishu_PIC = "https://telegra.ph/file/127df9ef604ba155ead6a.jpg"

perf = "Շђคภ๏ร קг๏"

async def killer():
    rishu_USER = Config.ALIVE_NAME
    name = f"{Config.ALIVE_NAME}'s Assistant"
    description = (
        f"I am Assistant Of {Config.ALIVE_NAME}.This Bot Can Help U To Chat With My Master"
    )
    bot_name = "THANOS"
    botname = f"{Config.BOT_USERNAME}"
    if bot_name.endswith("Assistant"):
        print("Bot Starting")
    else:
        try:
            await bot.send_message("@BotFather", "/setinline")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", perf)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", "/setname")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", name)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", "/setdescription")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", description)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", "/setuserpic")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_file("@BotFather", "THANOSPRO/resources/pics/main.jpg")
            await asyncio.sleep(2)
        except Exception as e:
            print(e)

# Client Starter
async def rishus(session=None, client=None, session_name="Main"):
    if session:
        LOGS.info(f"⚡️Starting Client [{session_name}] ⚡️")
        try:
            await client.start()
            return 1
        except:
            LOGS.error(f"Error in {session_name}!! Check & try again!")
            return 0
    else:
        return 0


# Load plugins based on config UNLOAD
async def plug_load(path):
    files = glob.glob(path)
    for name in files:
        with open(name) as rishu:
            path1 = Path(rishu.name)
            shortname = path1.stem
            if shortname.replace(".py", "") in Config.UNLOAD:
                os.remove(Path(f"THANOSPRO/plugins/{shortname}.py"))
            else:
                load_module(shortname.replace(".py", ""))      


# Final checks after startup
async def rishu_is_on(total):
    await update_sudo()
    await logger_check(bot)
    await start_msg(tbot, rishu_PIC, rishuver, total)
    await join_it(bot)
    await join_it(H2)
    await join_it(H3)
    await join_it(H4)
    await join_it(H5)


# THANOSPRO starter...

async def start_THANOSPRO():
    try:
        tbot_id = await tbot.get_me()
        Config.BOT_USERNAME = f"@{tbot_id.username}"
        bot.tgbot = tbot
        LOGS.info("⚡️ Starting Շђคภ๏รקг๏ ⚡️")
        C1 = await rishus(Config.THANOSPRO_SESSION, bot, "THANOSPRO_SESSION")
        C2 = await rishus(Config.SESSION_2, H2, "SESSION_2")
        C3 = await rishus(Config.SESSION_3, H3, "SESSION_3")
        C4 = await rishus(Config.SESSION_4, H4, "SESSION_4")
        C5 = await rishus(Config.SESSION_5, H5, "SESSION_5")
        await tbot.start(bot_token=Config.BOT_TOKEN)
        total = C1 + C2 + C3 + C4 + C5
        LOGS.info("⚡️Շђคภ๏รקг๏ Startup Completed ⚡️")
        LOGS.info("⚡️  installing Շђคภ๏รקг๏ Plugins ⚡️")
        await plug_load("THANOSPRO/plugins/*.py")
        await plug_channel(bot, Config.PLUGIN_CHANNEL)
        await killer()
        LOGS.info("⚡ Your Շђคภ๏รקг๏ Is Now Working ⚡")
        print("╭────⇌тнαησѕ⇋────")
        print("⚡️Starting thanos Mode!⚡️")
        print("⚡️ thanos Has Been Deployed Successfully ⚡️")
        print("⚡️Group⚡️ - @thanospross")
        print("╰────⇌тнαησѕ⇋────")
        LOGS.info(f"» Total Clients = {str(total)} «")
        await rishu_is_on(total)
    except Exception as e:
        LOGS.error(f"{str(e)}")
        sys.exit()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_THANOSPRO())

if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    try:
        bot.run_until_disconnected()
    except ConnectionError:
        pass


# THANOSPRO
