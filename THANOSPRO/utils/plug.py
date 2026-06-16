import asyncio
import datetime
import importlib
import inspect
import logging
import math
import os
import re
import sys
import time
import traceback
from pathlib import Path
from time import gmtime, strftime

from telethon import events
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator, InputMessagesFilterDocument

import THANOSPRO
from THANOSPRO.state import LOAD_PLUG
from THANOSPRO.config import Config
from THANOSPRO.clients.session import rishu, H2, H3, H4, H5, THANOSPRO_BOT
# Import helpers and utils inside functions to avoid circular issues


# ENV
ENV = bool(os.environ.get("ENV", False))
if ENV:
    from THANOSPRO.config import Config
else:
    if os.path.exists("Config.py"):
        from Config import Development as Config


# load plugins
def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import THANOSPRO.utils

        path = Path(f"THANOSPRO/plugins/{shortname}.py")
        name = "THANOSPRO.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info("THANOSPRO - Successfully imported " + shortname)
    else:
        import THANOSPRO.utils

        path = Path(f"THANOSPRO/plugins/{shortname}.py")
        name = "THANOSPRO.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        from THANOSPRO.clients import session
        from THANOSPRO.utils import utils, decorators, funcs, startup
        from THANOSPRO.helpers import int_str

        mod.bot = session.rishu
        mod.H1 = session.rishu
        mod.H2 = session.H2
        mod.H3 = session.H3
        mod.H4 = session.H4
        mod.H5 = session.H5
        mod.rishu = session.rishu
        mod.THANOSPRO = session.THANOSPRO_BOT
        mod.tbot = session.THANOSPRO_BOT
        mod.tgbot = THANOSPRO.bot.tgbot if THANOSPRO.bot else None
        # mod.command = command # command is not defined here
        # mod.CmdHelp = CmdHelp # CmdHelp is not defined here
        # mod.client_id = client_id # client_id is not defined here
        mod.logger = logging.getLogger(shortname)
        # support for uniborg
        sys.modules["uniborg.util"] = THANOSPRO.utils
        mod.Config = Config
        mod.borg = THANOSPRO.bot
        mod.THANOSPRO = THANOSPRO.bot
        # mod.edit_or_reply = edit_or_reply
        # mod.eor = edit_or_reply
        # mod.delete_rishu = delete_rishu
        # mod.eod = delete_rishu
        mod.Var = Config
        # mod.admin_cmd = admin_cmd
        # mod.rishu_cmd = rishu_cmd
        # mod.sudo_cmd = sudo_cmd
        # support for other userbots
        sys.modules["userbot.utils"] = THANOSPRO.utils
        sys.modules["userbot"] = THANOSPRO
        # support for paperplaneextended
        sys.modules["userbot.events"] = THANOSPRO
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            THANOSPRO.LOGS.error(f"Failed to load plugin {shortname}: {e}")
            return
        # for imports
        sys.modules["THANOSPRO.plugins." + shortname] = mod
        LOGS.info("⚡ Շђคภ๏ร-קг๏ ⚡ - Successfully Imported " + shortname)


# remove plugins
def remove_plugin(shortname):
    try:
        try:
            for i in LOAD_PLUG[shortname]:
                THANOSPRO.bot.remove_event_handler(i)
            del LOAD_PLUG[shortname]

        except BaseException:
            name = f"THANOSPRO.plugins.{shortname}"

            for i in reversed(range(len(THANOSPRO.bot._event_builders))):
                ev, cb = THANOSPRO.bot._event_builders[i]
                if cb.__module__ == name:
                    del THANOSPRO.bot._event_builders[i]
    except BaseException:
        raise ValueError


async def plug_channel(client, channel):
    if channel:
        LOGS.info("⚡ Շђคภ๏ร-קг๏ ⚡ - PLUGIN CHANNEL DETECTED.")
        LOGS.info("⚡ Շђคภ๏ร-קг๏ ⚡ - Starting to load extra plugins.")
        plugs = await client.get_messages(channel, None, filter=InputMessagesFilterDocument)
        total = int(plugs.total)
        for plugins in range(total):
            plug_id = plugs[plugins].id
            plug_name = plugs[plugins].file.name
            if os.path.exists(f"THANOSPRO/plugins/{plug_name}"):
                return
            downloaded_file_name = await client.download_media(
                await client.get_messages(channel, ids=plug_id),
                "THANOSPRO/plugins/",
            )
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            try:
                load_module(shortname.replace(".py", ""))
            except Exception as e:
                LOGS.error(str(e))


# THANOSPRO
