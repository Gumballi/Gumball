import glob
import asyncio
import os
import sys
import datetime
import random
import time
from pathlib import Path

# Fix potential circular imports by importing from state first
import THANOSPRO
from THANOSPRO.state import StartTime
from THANOSPRO import LOGS, validate_config, init_heroku
from THANOSPRO.config import Config
from THANOSPRO.clients.session import init_all_clients
from THANOSPRO.sql import init_db
from THANOSPRO.utils.plug import load_module, plug_channel
from THANOSPRO.utils.startup import logger_check, start_msg, update_sudo, join_it
from THANOSPRO.version import __rishu__ as rishuver

rishu_PIC = "https://telegra.ph/file/127df9ef604ba155ead6a.jpg"
perf = "Շђคภ๏ร קг๏"

async def killer(bot):
    name = f"{Config.ALIVE_NAME}'s Assistant"
    description = f"I am Assistant Of {Config.ALIVE_NAME}. This Bot Can Help U To Chat With My Master"
    botname = f"{Config.BOT_USERNAME}"
    
    try:
        await bot.send_message("@BotFather", "/setinline")
        await asyncio.sleep(1)
        await bot.send_message("@BotFather", botname)
        await asyncio.sleep(1)
        await bot.send_message("@BotFather", perf)
        # ... other BotFather commands ...
    except Exception as e:
        print(f"Error in killer: {e}")

async def plug_load(path):
    files = glob.glob(path)
    for name in files:
        path1 = Path(name)
        shortname = path1.stem
        if shortname == "__init__":
            continue
        if shortname in Config.UNLOAD:
            try:
                os.remove(name)
            except:
                pass
        else:
            try:
                load_module(shortname)
            except Exception as e:
                LOGS.error(f"Error loading {shortname}: {e}")

async def start_THANOSPRO():
    global StartTime
    THANOSPRO.state.StartTime = time.time()
    
    # 1. Validate Config
    validate_config()
    
    # 2. Init Heroku
    init_heroku()
    
    # 3. Init Database
    init_db()
    
    # 4. Init Clients
    rishu, tbot, multi_clients = init_all_clients()
    
    # Set global references in THANOSPRO module
    THANOSPRO.bot = rishu
    THANOSPRO.tbot = tbot
    
    try:
        LOGS.info("⚡️ Starting Շђคภ๏รקг๏ ⚡️")
        
        # Start Userbot
        await rishu.start()
        C1 = 1
        
        # Start Bot
        await tbot.start(bot_token=Config.BOT_TOKEN)
        
        # Start Multi Clients
        total = C1
        for name, client in multi_clients.items():
            if client:
                try:
                    await client.start()
                    total += 1
                except Exception as e:
                    LOGS.error(f"Error starting {name}: {e}")

        tbot_id = await tbot.get_me()
        Config.BOT_USERNAME = f"@{tbot_id.username}"
        rishu.tgbot = tbot
        
        LOGS.info("⚡️Շђคภ๏รקг๏ Startup Completed ⚡️")
        LOGS.info("⚡️ Installing Շђคภ๏รקг๏ Plugins ⚡️")
        
        await plug_load("THANOSPRO/plugins/*.py")
        await plug_channel(rishu, Config.PLUGIN_CHANNEL)
        
        # await killer(tbot) # Optional: update bot profile
        
        LOGS.info("⚡ Your Շђคภ๏รקг๏ Is Now Working ⚡")
        print("╭────⇌тнαησѕ⇋────")
        print("⚡️Starting thanos Mode!⚡️")
        print("⚡️ thanos Has Been Deployed Successfully ⚡️")
        print("⚡️Group⚡️ - @thanospross")
        print("╰────⇌тнαησѕ⇋────")
        LOGS.info(f"» Total Clients = {str(total)} «")
        
        # Final checks
        await update_sudo()
        await logger_check(rishu)
        await start_msg(tbot, rishu_PIC, rishuver, total)
        await join_it(rishu)
        for client in multi_clients.values():
            if client:
                await join_it(client)
                
    except Exception as e:
        LOGS.error(f"Startup failed: {e}")
        sys.exit(1)

async def main():
    await start_THANOSPRO()
    if THANOSPRO.bot:
        try:
            await THANOSPRO.bot.run_until_disconnected()
        except ConnectionError:
            pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        LOGS.error(f"Fatal error: {e}")
        sys.exit(1)
