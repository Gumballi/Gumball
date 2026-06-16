import datetime
import random
import time

from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot

from . import *
from THANOSPRO.sql.gvar_sql import gvarstat
from THANOSPRO.state import StartTime

#-------------------------------------------------------------------------------


msg = """THANOS IS ALIVE
**╭────⇌тнαησѕ⇋────**
◈┈˃̶ тнαησѕ ~ v2\n
◈┈˃̶ Շђคภ๏ร   ~ [๏ฬภєг](https://t.me/THANOSCEO)\n
◈┈˃̶ รยקק๏гՇ ~ [Group](https://t.me/+cJG1PbKtpPVmNDg5)\n
◈┈˃̶ яєρσ   ~ [Repo](https://github.com/thanosuser/THANOS-PRO)
**╰────⇌тнαησѕ⇋────**
"""
#-------------------------------------------------------------------------------


@rishu_cmd(pattern="alive87644$")
async def up(event):
    cid = await client_id(event)
    ultronceo, rishu_USER, rishu_mention = cid[0], cid[1], cid[2]
    start = datetime.datetime.now()
    rishu = await eor(event, "`Building Alive....`")
    uptime = await get_time((time.time() - StartTime))
    a = gvarstat("ALIVE_PIC")
    pic_list = []
    if a:
        b = a.split(" ")
        if len(b) >= 1:
            for c in b:
                pic_list.append(c)
        PIC = random.choice(pic_list)
    else:
        PIC = "https://telegra.ph/file/ea9e11f7c9db21c1b8d5e.mp4"
    end = datetime.datetime.now()
    ling = (end - start).microseconds / 1000
    omk = ALIVE_TEMP.format(ultronceo, rishu_USER, tel_ver, rishu_ver, is_sudo, uptime, ling)
    await event.client.send_file(event.chat_id, file=PIC, caption=omk, parse_mode="HTML")
    await rishu.delete()



@rishu_cmd(pattern="rishuuuus$")
async def rishu_a(event):
    cid = await client_id(event)
    ultronceo, rishu_USER, rishu_mention = cid[0], cid[1], cid[2]
    uptime = await get_time((time.time() - StartTime))
    am = gvarstat("ALIVE_MSG") or "<b>»» Շђคภ๏รקг๏ ιѕ σиℓιиє ««</b>"
    try:
        rishu = await event.client.inline_query(Config.BOT_USERNAME, "alive")
        await rishu[0].click(event.chat_id)
        if event.sender_id == ultronceo:
            await event.delete()
    except (noin, dedbot):
        await eor(event, msg.format(am, tel_ver, rishu_ver, uptime, abuse_m, is_sudo), parse_mode="HTML")

file1 = "https://telegra.ph/file/b4b1e6f42dec529c86011.mp4"
file2 = "https://telegra.ph/file/19a2f441d5b8f37657a21.mp4"
file3 = "https://telegra.ph/file/19a2f441d5b8f37657a21.mp4"
file4 = "https://telegra.ph/file/b4b1e6f42dec529c86011.mp4"
file5 = "https://telegra.ph/file/b4b1e6f42dec529c86011.mp4"
"""=======================CONSTANTS====================== """
pm_caption = f"**╭────⇌тнαησѕ⇋────**\n"
pm_caption += f"◈┈˃̶ ๏ฬภєг   ~ {Config.ALIVE_NAME}\n"
pm_caption += f"◈┈˃̶ тнαησѕ ~ v2.0.1\n"
pm_caption += f"◈┈˃̶ Շђคภ๏ร๒๏ץ   ~ [๏ฬภєг](https://t.me/THANOSCEO)\n"
pm_caption += f"◈┈˃̶ รยקק๏гՇ ~ [Group](https://t.me/+cJG1PbKtpPVmNDg5)\n"
pm_caption += f"◈┈˃̶ яєρσ   ~ [Repo](https://github.com/thanosuser/THANOS-PRO)\n"
pm_caption += f"**╰────⇌тнαησѕ⇋────**\n"


@rishu_cmd(pattern="alive$")
async def amireallyalive(yes):
    edit_time = 12
    reply_to_id = await reply_id(yes)
    await yes.get_chat()
    on = await yes.client.send_file(
        yes.chat_id, file=file1, caption=pm_caption, reply_to=reply_to_id
    )
    await asyncio.sleep(edit_time)
    ok = await yes.client.edit_message(yes.chat_id, on, file=file2)

    await asyncio.sleep(edit_time)
    ok2 = await yes.client.edit_message(yes.chat_id, ok, file=file3)

    await asyncio.sleep(edit_time)
    ok3 = await yes.client.edit_message(yes.chat_id, ok2, file=file4)

    await asyncio.sleep(edit_time)
    ok4 = await yes.client.edit_message(yes.chat_id, ok3, file=file5)

    await asyncio.sleep(edit_time)
    ok5 = await yes.client.edit_message(yes.chat_id, ok4, file=file4)

    await asyncio.sleep(edit_time)
    ok6 = await yes.client.edit_message(yes.chat_id, ok5, file=file3)

    await asyncio.sleep(edit_time)
    ok7 = await yes.client.edit_message(yes.chat_id, ok6, file=file2)

    await asyncio.sleep(edit_time)
    ok8 = await yes.client.edit_message(yes.chat_id, ok7, file=file1)

    await asyncio.sleep(edit_time)
    ok9 = await yes.client.edit_message(yes.chat_id, ok8, file=file2)

    await asyncio.sleep(edit_time)
    ok10 = await yes.client.edit_message(yes.chat_id, ok9, file=file3)

    await asyncio.sleep(edit_time)
    ok11 = await yes.client.edit_message(yes.chat_id, ok10, file=file4)

    await asyncio.sleep(edit_time)
    ok12 = await yes.client.edit_message(yes.chat_id, ok11, file=file5)

    await asyncio.sleep(edit_time)
    ok13 = await yes.client.edit_message(yes.chat_id, ok12, file=file1)

    await yes.delete()

    """ For .alive command, check if the bot is running.  """
    await event.client.send_file(alive.chat_id, PM_IMG, caption=pm_caption)
    await alive.delete()

CmdHelp("alive").add_command(
  "alive", None, "Shows the Default Alive Message"
).add_warning(
  "✅ Harmless Module"
).add()
