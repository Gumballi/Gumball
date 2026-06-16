import asyncio
from . import *

# URLs and captions
ok = "https://telegra.ph/file/f092c5e302854f146da74.jpg"
ok1 = 'https://telegra.ph/file/bfee4639f6d0e777f11d4.jpg'
ok2 = "https://telegra.ph/file/0a1f4dd861247158d1c78.jpg"
ok3 = "https://telegra.ph/file/2f198cfb45b7dae3e7b67.jpg"
ok4 = "https://telegra.ph/file/d8dfff58472681c196a10.jpg"
ok5 = "https://telegra.ph/file/d7663a8372268c4e066a9.jpg"
ok6 = "https://telegra.ph/file/1901fd8c1dbe69527c280.jpg"
ok7 = "https://telegra.ph/file/069b3be8f57b84e8c8001.jpg"
ok8 = "https://telegra.ph/file/c6e15e553c519bef360e9.jpg"
ok9 = "https://telegra.ph/file/fac51f7b738a122a2222b.jpg"
ok10 = "https://telegra.ph/file/4dce355acbb2c057309a4.jpg"
ok11 = "https://telegra.ph/file/f2dd6742417c0d7ae7ce2.jpg"
ok12 = "https://telegra.ph/file/cadf5668940c07f9d9bba.jpg"
ok13 = "https://telegra.ph/file/8f88d3f8919c617da78d9.jpg"
ok14 = "https://telegra.ph/file/07f7154e2f733fb0181ba.jpg"
ok15 = "https://telegra.ph/file/5e1e97e558f073ea36b54.jpg"
ok16 = "https://telegra.ph/file/a21b08e83dd7c476aae64.jpg"
ok17 = "https://telegra.ph/file/2d37ca276751e846b1c7b.jpg"

caps = [
    (ok, "CHUP RNDI"),
    (ok1, "TU CHUP HOGA YA TERI GAND M SRIA DU BETICHOD"),
    (ok2, "RANDI AURAT"),
    (ok3, "CHUT KA PIYASA AADMI"),
    (ok4, "FULL RAMDIBAAZI BHIYA"),
    (ok5, "WHAT'S NEW I ALREADY KNEW"),
    (ok6, "I TRIED SO HARD AND GO SO FAR"),
    (ok7, "BUT IN THE END"),
    (ok8, "IT DOES NOT EVEN MATTER"),
    (ok9, "CHEEMS IS LOVE"),
    (ok10, "I KNOW I M PRO"),
    (ok11, "LOOK WHAT U DID"),
    (ok12, "TWO MINUTES SILENCE PLIMS"),
    (ok13, "AAGE JAKE GAND MRAWA BHOSDIWALE"),
    (ok14, "FULL SUPPORT"),
    (ok15, "YAR MEIN ITNA COOL KYU HU YAAR"),
    (ok16, "U MAH LOMVE"),
    (ok17, "CHEEMS IS LOVE")
]

@rishu_cmd(pattern="cb")
async def _(event):
    await event.delete()
    reply_to = await reply_id(event)
    
    first_pic, first_cap = caps[0]
    msg = await event.client.send_file(event.chat_id, first_pic, caption=first_cap, reply_to=reply_to)
    
    for pic, cap in caps[1:]:
        await asyncio.sleep(4)
        await event.client.edit_message(event.chat_id, msg, cap, file=pic)

CmdHelp("cheemsbaazi").add_command(
  "cb", None, "tag someone and see"
).add_warning(
  "✅ Harmless Module"
).add()
