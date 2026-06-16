#thanospross 
# 18+ shayri

import asyncio
import random

from . import *
from THANOSPRO.utils import admin_cmd

DEFAULTUSER = str(Config.ALIVE_NAME) if Config.ALIVE_NAME else "@thanosceo"



@rishu_cmd(pattern=r"ashayri$")
async def _(event):
    if event.fwd_from:
        return
    await event.edit(" Making A Shayri.......")
    await asyncio.sleep(1.3)
    h = random.randrange(1, 9)
    if h == 1:
        await event.edit(
            f"HM TANHAYI M APNA,\nAPNA SAB KUSH GAWA BETHE,\nWO TO KHOGYI KISI OR KE PYAR MIEN.\nHAM APNE JHATO M AAG LGA BETHE.\n\n\n✍️ {DEFAULTUSER}"
        )
    if h == 2:
        await event.edit(
            f"WO MAJA NA TKHT MIEN,\nNA TAJ MIEN.\nNA KUBER KE DHAN MIEN,\nJO MAJA H SUBH UTHKE AND KHUJANE MIEN.\n\n\n✍️ {DEFAULTUSER}"
        )
    if h == 3:
        await event.edit(
            f"HMNE TO WAFA KI THI OSEENE DIL TODA MERA EK DIN AKE PUSHNE LAGI YAD ATI H HMARI?HMNE B KHEDIYA AJII LWDA MERA.\n\n\n✍️{DEFAULTUSER}"
        )
    if h == 4:
        await event.edit(
            f"SEX KRNE M WO MJA KHAN AYE JO AWE LULI HILANE MIEN.\n\nEK MNT M KAM HO JAYE OR PHR SHUTI SBSE BDIYA H APNI MUTHI .\n\n\n✍️{DEFAULTUSER}"
        )
    if h == 5:
        await event.edit(
            f"SUBH KA PHELA KHWAB RAT KI ANTIM YAD HO TUM,\n KYA KARE AB HM B JANAB,\n WO TERI CHUCHI KI YAD TDFATI HAI, \nWO KALI JHAT M GULABI CHUT BADI YAD ATI H.\n\n\n✍️{DEFAULTUSER}"
        )
    if h == 6:
        await event.edit(
            f"KHETI H DHEERE SE DALIYE SAJNA..../nBALO KE BEECH FOOL GULAB KA..... \nKHTA H JAB DALTA HUN....... \nTO JHAD JATA H PATA PATA GULAB KA.....\n\n\n✍️{DEFAULTUSER}"
        )
    if h == 7:
        await event.edit(
            f"AAJ PHR ONKI YAD AGYI...\nPHR KYA THAA..\nHATH M LIYA LWDA HILAYA OSKE NAM KA.\n\n\n✍️{DEFAULTUSER}  "
        )
    if h == 8:
        await event.edit(
            f"WO B KYA DIN THE,\nJAB TU KHTI THI KI ABI NAHI SHADI BAD KRNGE, l,\nAB TO TU ROJ NYA BNDA BNATI H,\n PHR KPDE PHENTI H OSE BHOOL JATI H .\n\n\n✍️{DEFAULTUSER}"
        )
    if h == 9:
        await event.edit(
            f"EK DIN RASTE SE JA RHA THA,\nTUJE DEKHTE H PHELI NAJR M PYAR HOGYA, \nOR PHR KUSH MHENO BAD\n MUJE PAPA KHENE WALA AGYA…\n\n\n✍️{DEFAULTUSER}"
        )

CmdHelp("adultsahyri").add_command(
  "ashayri", None, "adult sahyri"
).add_warning(
  "✅ Harmless Module"
).add()
