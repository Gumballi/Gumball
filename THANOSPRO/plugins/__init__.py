import datetime
import time
import THANOSPRO
from THANOSPRO.config import Config
from THANOSPRO.version import __rishu__
from telethon import version

# Use delayed imports for helpers and utils inside functions
# from THANOSPRO.sql.gvar_sql import gvarstat

rishu_logo = "./THANOSPRO/resources/pics/THANOSPRO_logo.jpg"
cjb = "./THANOSPRO/resources/pics/cjb.jpg"
restlo = "./THANOSPRO/resources/pics/rest.jpeg"
shuru = "./THANOSPRO/resources/pics/shuru.jpg"
shhh = "./THANOSPRO/resources/pics/chup_madarchod.jpeg"

hl = Config.HANDLER
shl = Config.SUDO_HANDLER
rishu_ver = __rishu__
tel_ver = version.__version__

async def get_user_id(ids):
    if str(ids).isdigit():
        userid = int(ids)
    else:
        userid = (await THANOSPRO.bot.get_entity(ids)).id
    return userid

# Move dynamic variables to properties or functions
def get_abuse_status():
    abus = Config.ABUSE
    return "Enabled" if abus == "ON" else "Disabled"

my_channel = Config.MY_CHANNEL or "thanospros"
my_group = Config.MY_GROUP or "THANOSPRO_Chat"
if "@" in my_channel:
    my_channel = my_channel.replace("@", "")
if "@" in my_group:
    my_group = my_group.replace("@", "")

chnl_link = "https://t.me/thanospros"
rishu_channel = f"[Շђคภ๏ร-קг๏]({chnl_link})"
grp_link = "https://t.me/THANOSPRO_Chat"
rishu_grp = f"[Շђคภ๏ร-קг๏ Group]({grp_link})"

WELCOME_FORMAT = """**Use these formats in your welcome note to make them attractive.**
  {mention} :  To mention the user
  {title} : To get chat name in message
  {count} : To get group members
  {first} : To use user first name
  {last} : To use user last name
  {fullname} : To use user full name
  {userid} : To use userid
  {username} : To use user username
  {my_first} : To use my first name
  {my_fullname} : To use my full name
  {my_last} : To use my last name
  {my_mention} : To mention myself
  {my_username} : To use my username
"""

# Re-export core decorators for easy access in plugins
from THANOSPRO.clients.decs import rishu_cmd, rishu_handler
from THANOSPRO.utils.extras import edit_or_reply, delete_rishu
eor = edit_or_reply
eod = delete_rishu

# Re-export state variables
from THANOSPRO.state import StartTime, CMD_HELP, CMD_LIST
from THANOSPRO.utils.plug import CmdHelp
