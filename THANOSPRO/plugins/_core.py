import asyncio
import io
import os

from datetime import datetime
from pathlib import Path

from telethon import events, functions, types
from telethon.tl.types import InputMessagesFilterDocument

from . import *


@rishu_cmd(pattern="cmds$")
async def list_plugins(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    cids = await client_id(event)
    ultronceo, rishu_USER, rishu_mention = cids[0], cids[1], cids[2]
    
    plugins = []
    for file in os.listdir("THANOSPRO/plugins"):
        if file.endswith(".py") and not file.startswith("__"):
            plugins.append(file.replace(".py", ""))
    
    o = "\n".join(sorted(plugins))
    OUTPUT = f"""
<h1>List of Plugins in Շђคภ๏ร-קг๏:</h1>

<code>{o}</code>

<b><i>HELP:</b></i> <i>If you want to know the commands for a plugin, do “ .plinfo <plugin name> ”

<b><a href='https://t.me/thanospros'>@thanospros</a></b>
"""
    rishu = await telegraph_paste("All available plugins in Շђคภ๏ร-קг๏", OUTPUT)
    await eor(event, f"[All available plugins in Շђคภ๏ร-קг๏]({rishu})", link_preview=False)


@rishu_cmd(pattern="send ([\s\S]*)")
async def send_plugin(event):
    cids = await client_id(event)
    ultronceo, rishu_USER, rishu_mention = cids[0], cids[1], cids[2]
    message_id = event.reply_to_msg_id or event.message.id
    thumb = rishu_logo
    input_str = event.pattern_match.group(1).strip()
    omk = f"**• Plugin name ≈** `{input_str}`\n**• Uploaded by ≈** {rishu_mention}\n\n⚡ **[ʟɛɢɛռɖaʀʏ ᴀғ Շђคภ๏รקг๏]({chnl_link})** ⚡"
    the_plugin_file = "./THANOSPRO/plugins/{}.py".format(input_str.lower())
    if os.path.exists(the_plugin_file):
        await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            thumb=thumb,
            caption=omk,
            force_document=True,
            allow_cache=False,
            reply_to=message_id,
        )
        await event.delete()
    else:
        await eod(event, "File not found..... Kek")


@rishu_cmd(pattern="install(?:\s|$)([\s\S]*)")
async def install(event):
    cids = await client_id(event)
    ultronceo, rishu_USER, rishu_mention = cids[0], cids[1], cids[2]
    b = 1
    owo = event.pattern_match.group(1).strip()
    rishu = await eor(event, "__Installing.__")
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(
                await event.get_reply_message(),
                "./THANOSPRO/plugins/"
            )
            if owo != "-f":
                with open(downloaded_file_name, "r") as op:
                    rd = op.read()
                try:
                    for harm in HARMFUL:
                        if harm in rd:
                            os.remove(downloaded_file_name)
                            return await rishu.edit(f"**⚠️ WARNING !!** \n\n__Replied plugin file contains some harmful codes. Please consider checking the file. If you still want to install then use__ `{hl}install -f`. \n\n**Codes Detected :** \n• {harm}")
                except BaseException:
                    pass
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                if shortname in CMD_LIST:
                    string = "**Commands found in** `{}`\n".format((os.path.basename(downloaded_file_name)))
                    for i in CMD_LIST[shortname]:
                        string += "  •  `" + i 
                        string += "`\n"
                        if b == 1:
                            a = "__Installing..__"
                            b = 2
                        else:
                            a = "__Installing...__"
                            b = 1
                        await rishu.edit(a)
                    return await rishu.edit(f"✅ **Installed module** :- `{shortname}` \n✨ BY :- {rishu_mention}\n\n{string}\n\n        ⚡ **[ʟɛɢɛռɖaʀʏ ᴀғ Շђคภ๏รקг๏]({chnl_link})** ⚡", link_preview=False)
                return await rishu.edit(f"Installed module `{os.path.basename(downloaded_file_name)}`")
            else:
                os.remove(downloaded_file_name)
                return await eod(rishu, f"**Failed to Install** \n`Error`\nModule already installed or unknown format")
        except Exception as e: 
            await eod(rishu, f"**Failed to Install** \n`Error`\n{str(e)}")
            if 'downloaded_file_name' in locals() and os.path.exists(downloaded_file_name):
                os.remove(downloaded_file_name)


@rishu_cmd(pattern="uninstall ([\s\S]*)")
async def uninstall(event):
    shortname = event.pattern_match.group(1).strip()
    if ".py" in shortname:
        shortname = shortname.replace(".py", "")
    rishu = await eor(event, f"__Trying to uninstall plugin__ `{shortname}` ...")
    dir_path =f"./THANOSPRO/plugins/{shortname}.py"
    try:
        remove_plugin(shortname)
        if os.path.exists(dir_path):
            os.remove(dir_path)
        await eod(rishu, f"**Uninstalled plugin** `{shortname}` **successfully.**")
    except OSError as e:
        await eod(rishu, f"**Error !!** \n\n`{dir_path}` : __{e.strerror}__")


@rishu_cmd(pattern="unload ([\s\S]*)")
async def unload(event):
    shortname = event.pattern_match.group(1).strip()
    try:
        remove_plugin(shortname)
        await event.edit(f"Successfully unloaded `{shortname}`")
    except Exception as e:
        await event.edit(f"Failed to unload {shortname}\n{str(e)}")


@rishu_cmd(pattern="load ([\s\S]*)")
async def load(event):
    shortname = event.pattern_match.group(1).strip()
    try:
        try:
            remove_plugin(shortname)
        except BaseException:
            pass
        load_module(shortname)
        await event.edit(f"Successfully loaded `{shortname}`")
    except Exception as e:
        await event.edit(
            f"Sorry, could not load {shortname} because of the following error.\n{str(e)}"
        )

CmdHelp("core").add_command(
  "install", "<reply to a .py file>", "Installs the replied python file if suitable to Շђคภ๏ร-קг๏'s codes.`\n**🚩 Flags :** `-f"
).add_command(
  "uninstall", "<plugin name>", "Uninstalls the given plugin from Շђคภ๏ร-קг๏. To get that again do .restart", "uninstall alive"
).add_command(
  "load", "<plugin name>", "Loades the unloaded plugin to your userbot", "load alive"
).add_command(
  "unload", "<plugin name>", "Unloads the plugin from your userbot", "unload alive"
).add_command(
  "send", "<file name>", "Sends the given file from your userbot server, if any.", "send alive"
).add_command(
  "cmds", None, "Gives out the list of modules in THANOSPRO."
).add_command(
  "repo", None, "Gives THANOSPRO's Github repo link."
).add_command(
  "help", None, "Shows inline help menu."
).add_command(
  "plinfo", "<plugin name>", "Shows the detailed information of given plugin."
).add_command(
  "cmdinfo", "<cmd name>", "Shows the information of given command."
).add_warning(
  "❌ Install External Plugin On Your Own Risk. We won't help if anything goes wrong after installing a plugin."
).add()
