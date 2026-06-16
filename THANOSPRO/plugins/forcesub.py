from telethon.events import InlineQuery, callbackquery
from telethon import Button, events
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest
import re

from THANOSPRO.sql.fsub_sql import *
from . import *

@H1.on(events.ChatAction())
async def forcesub(event):
    if all_fsub() == None:
        return
    if not (event.user_joined or event.user_added):
        return
    if not is_fsub(event.chat_id):
        return
    user = await event.get_user()
    if user.bot:
        return
    xyz = is_fsub(event.chat_id)
    joinchat = xyz.channel
    try:
        await event.client(GetParticipantRequest(int(joinchat), user.id))
    except UserNotParticipantError:
        await event.client.edit_permissions(event.chat_id, user.id, send_messages=False)
        channel = await event.client.get_entity(int(joinchat))
        user_entity = await event.client.get_entity(int(user.id))
        if not channel.username:
            channel_link = (await event.client(ExportChatInviteRequest(channel))).link
        else:
            channel_link = "https://t.me/" + channel.username
        capt = f"**👋 Welcome** [{user_entity.first_name}](tg://user?id={user_entity.id}), \n\n**📍 You need to Join** {channel.title} **to chat in this group.**"
        btns = [Button.url("Channel", url=channel_link), Button.inline("Unmute Me", data=f"unmute_{user_entity.id}")]
        await tbot.send_message(event.chat_id, capt, buttons=btns)

@rishu_cmd(pattern="fsub(?:\s|$)([\s\S]*)")
async def _(event):
    if event.is_private:
        await eor(event, "This is meant to be used in groups only!!")
        return
    hunter = event.pattern_match.group(1)
    if not hunter:
        return await eod(event, "Need a Channel Username Or Channel ID 🥴")
    if hunter.startswith("@"):
        ch = hunter
    else:
        try:
            ch = int(hunter)
        except BaseException:
            return await eod(event, "⚠️ **Error !** \n\nChannel ID invalid. Please Recheck It !")
    try:
        hunter_id = (await event.client.get_entity(ch)).id
    except BaseException:
        return await eod(event, "⚠️ **Error !** \n\nChannel ID invalid. Please Recheck It !")
    
    if not str(hunter_id).startswith("-100"):
        # This logic is a bit flawed for some IDs but keeping it as per original intent
        pass
        
    add_fsub(event.chat_id, hunter_id)
    await eor(event, "Implementing **Force Subscribe** In This Channel !!")

@rishu_cmd(pattern="rmfsub$")
async def removef(event):
    if is_fsub(event.chat_id):
        rm_fsub(event.chat_id)
        await eor(event, "Deactivated **Force Subscribe** In This Channel !!")
    else:
        return await eod(event, "I don't think force sub was activated here.")

@rishu_cmd(pattern="chfsub$")
async def getfsub(event):
    x = is_fsub(event.chat_id)
    if not x:
        return await eod(event, "Force Subscribe Is Disabled Here..")
    a = x.chat_id
    b = x.channel
    xx = await event.client.get_entity(int(a))
    yy = await event.client.get_entity(int(b))
    uname = f"@{xx.username}" if xx.username else "No Username"
    usern = f"@{yy.username}" if yy.username else "No Username"
    await eor(event, f"**ForceSub Enabled !!**\n\n» __Force Subscribe to__ {yy.title} ~ {usern} \n» __For Chat__ {xx.title} ~ {uname}")

@rishu_cmd(pattern="lsfsub$")
async def list_fsub(event):
    channels = all_fsub()
    CHANNEL_LIST = "**🚀 Fsub Enabled For & In :**\n\n"
    if channels and len(channels) > 0:
        for hunter in channels:
            a = hunter.chat_id
            b = hunter.channel
            try:
                xx = await event.client.get_entity(int(a))
                yy = await event.client.get_entity(int(b))
                uname = f"@{xx.username}" if xx.username else "No Username"
                usern = f"@{yy.username}" if yy.username else "No Username"
                CHANNEL_LIST += f"»» **FSub to ** [ {yy.title} ~ {usern} ] **in chat** [ {xx.title} {uname} ]\n"
            except:
                CHANNEL_LIST += f"»» **FSub to ** [ {b} ] **in chat** [ {a} ] (Entity not found)\n"
    else:
        CHANNEL_LIST = "No Chat Found With Active Force Subscribe."
    await eor(event, CHANNEL_LIST)

@tbot.on(events.CallbackQuery(data=re.compile(b"unmute_(.*)")))
async def unmute_callback(event):
    uid = int(event.data_match.group(1).decode("UTF-8"))
    fsub = is_fsub(event.chat_id)
    if not fsub:
        await event.answer("Force subscribe is not enabled here.", alert=True)
        return
    joinchat = fsub.channel
    if uid == event.sender_id:
        try:
            user_full = await event.client(GetFullUserRequest(uid))
            nm = user_full.user.first_name
        except:
            nm = "User"
            
        # Check participation using any available client
        clients = [H1, H2, H3, H4, H5, tbot]
        joined = False
        for client in clients:
            if client:
                try:
                    await client(GetParticipantRequest(int(joinchat), uid))
                    joined = True
                    break
                except UserNotParticipantError:
                    await event.answer("You need to join the channel first.", alert=True)
                    return
                except:
                    continue
        
        if not joined:
            await event.answer("Could not verify participation. Please try again later.", alert=True)
            return

        # Unmute using any available client
        unmuted = False
        for client in clients:
            if client:
                try:
                    await client.edit_permissions(event.chat_id, uid, until_date=None, send_messages=True)
                    unmuted = True
                    break
                except:
                    continue
        
        if unmuted:
            msg = f"**rishuo {nm} !! Welcome to {(await event.get_chat()).title} ✨**"
            await event.edit(msg)
        else:
            await event.answer("Failed to unmute. Please ask an admin.", alert=True)
    else:
        await event.answer("You are an old member and can speak freely! This isn't for you!", cache_time=0, alert=True)

CmdHelp("forcesub").add_command(
  "fsub", "<channel username/id>", "Activates Force Subscribe In The Chat"
).add_command(
  "rmfsub", None, "Removes the chat from Force Subscribe"
).add_command(
  "chfsub", None, "Checks for the Status of Force Subscribe In The Chat."
).add_command(
  "lsfsub", None, "Gives the list of all chats with force subscribe enabled."
).add_warning(
  "✅ Harmless Module."
).add_info(
  "Force Them To Join. \n**📌 Note :** You need to be admin jn both the chat to use this module."
).add()
