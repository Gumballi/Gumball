import asyncio
import io
import os
import time

from . import *

if not os.path.isdir("./SAVED"):
    os.makedirs("./SAVED")
if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)


@rishu_cmd(pattern="ls(?:\s|$)([\s\S]*)")
async def lst(event):
    input_str = event.pattern_match.group(1).strip()
    if input_str:
        if not os.path.exists(input_str):
            return await eod(event, f"Path `{input_str}` does not exist.")
        msg = "📂 **Files in {} :**\n".format(input_str)
        try:
            files = os.listdir(input_str)
        except Exception as e:
            return await eod(event, f"Error: `{str(e)}`")
    else:
        msg = "📂 **Files in Current Directory :**\n"
        files = os.listdir(os.getcwd())
    
    for file in sorted(files):
        msg += "📑 `{}`\n".format(file)
        
    if len(msg) <= Config.MAX_MESSAGE_SIZE_LIMIT:
        await eor(event, msg)
    else:
        msg = msg.replace("`", "")
        out_path = "filesList.txt"
        with open(out_path, "w") as f:
            f.write(msg)
        await event.client.send_file(
            event.chat_id,
            out_path,
            force_document=True,
            allow_cache=False,
            caption="`Output is huge. Sending as a file...`"
        )
        os.remove(out_path)
        await event.delete()


@rishu_cmd(pattern="ls_local$")
async def ls_local(event):
    cmd = "ls -lh ./DOWNLOADS/"
    reply_to_id = event.reply_to_msg_id or event.message.id
    
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    out = stdout.decode()
    err = stderr.decode()
    
    OUTPUT = f"**Files in Շђคภ๏ร-קг๏ DOWNLOADS Folder:**\n"
    if err:
        return await eor(event, f"**Error:** `{err}`")
        
    if len(out) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(out)) as out_file:
            out_file.name = "ls_local.txt"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=OUTPUT,
                reply_to=reply_to_id,
            )
            await event.delete()
    else:
        await eor(event, f"{OUTPUT}`{out}`")


@rishu_cmd(pattern="ls_root$")
async def ls_root(event):
    cmd = "ls -lh"
    reply_to_id = event.reply_to_msg_id or event.message.id
    
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    out = stdout.decode()
    err = stderr.decode()
    
    OUTPUT = f"**Files in root directory:**\n"
    if err:
        return await eor(event, f"**Error:** `{err}`")
        
    if len(out) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(out)) as out_file:
            out_file.name = "ls_root.txt"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=OUTPUT,
                reply_to=reply_to_id,
            )
            await event.delete()
    else:
        await eor(event, f"{OUTPUT}`{out}`")


@rishu_cmd(pattern="ls_saved$")
async def ls_saved(event):
    cmd = "ls -lh ./SAVED/"
    reply_to_id = event.reply_to_msg_id or event.message.id
    
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    out = stdout.decode()
    err = stderr.decode()
    
    OUTPUT = f"**Files in SAVED directory:**\n"
    if err:
        return await eor(event, f"**Error:** `{err}`")
        
    if len(out) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(out)) as out_file:
            out_file.name = "ls_saved.txt"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=OUTPUT,
                reply_to=reply_to_id,
            )
            await event.delete()
    else:
        await eor(event, f"{OUTPUT}`{out}`")


@rishu_cmd(pattern="rnsaved(?:\s|$)([\s\S]*)")
async def rename_saved(event):
    input_str = event.pattern_match.group(1).strip()
    if "|" not in input_str:
        return await eod(event, f"Usage: `{hl}rnsaved old_name | new_name`")
    
    src, dst = input_str.split("|")
    src = src.strip()
    dst = dst.strip()
    
    src_path = f"./SAVED/{src}"
    dst_path = f"./SAVED/{dst}"
    
    if not os.path.exists(src_path):
        return await eod(event, f"File `{src}` not found in SAVED.")
        
    try:
        os.rename(src_path, dst_path)
        await eor(event, f"File renamed `{src}` to `{dst}` in SAVED.")
    except Exception as e:
        await eod(event, f"Error: `{str(e)}`")


@rishu_cmd(pattern="rnlocal(?:\s|$)([\s\S]*)")
async def rename_local(event):
    input_str = event.pattern_match.group(1).strip()
    if "|" not in input_str:
        return await eod(event, f"Usage: `{hl}rnlocal old_name | new_name`")
    
    src, dst = input_str.split("|")
    src = src.strip()
    dst = dst.strip()
    
    src_path = f"./DOWNLOADS/{src}"
    dst_path = f"./DOWNLOADS/{dst}"
    
    if not os.path.exists(src_path):
        return await eod(event, f"File `{src}` not found in DOWNLOADS.")
        
    try:
        os.rename(src_path, dst_path)
        await eor(event, f"File renamed `{src}` to `{dst}` in DOWNLOADS.")
    except Exception as e:
        await eod(event, f"Error: `{str(e)}`")


@rishu_cmd(pattern="delsave(?:\s|$)([\s\S]*)")
async def del_save(event):
    input_str = event.pattern_match.group(1).strip()
    pathtofile = f"./SAVED/{input_str}"

    if os.path.isfile(pathtofile):
        os.remove(pathtofile)
        await eod(event, "✅ File Deleted 🗑")
    else:
        await eod(event, "⛔️File Not Found😬")


@rishu_cmd(pattern="delocal(?:\s|$)([\s\S]*)")
async def del_local(event):
    input_str = event.pattern_match.group(1).strip()
    pathtofile = f"./DOWNLOADS/{input_str}"

    if os.path.isfile(pathtofile):
        os.remove(pathtofile)
        await eod(event, "✅ File Deleted 🗑")
    else:
        await eod(event, "⛔️File Not Found😬")


CmdHelp("managers").add_command(
  "ls_local", None, "Gives the list of downloaded medias in your THANOSPRO server."
).add_command(
  "ls_root", None, "Gives the list of all files in root directory of THANOSPRO repo."
).add_command(
  "ls_saved", None, "Gives the list of all files in Saved directory of your THANOSPRO server"
).add_command(
  "rnsaved", "from | to", "Renames the file in saved directory"
).add_command(
  "rnlocal", "from | to", "Renames the file in downloaded directory"
).add_command(
  "delsave", "saved path", "Deletes the file from given saved path"
).add_command(
  "delocal", "downloaded path", "Deletes the file from given downloaded path"
).add_command(
  "ls", "<path name>", "Gives the list of all files in the given path"
).add_info(
  "THANOSPRO Managers."
).add_warning(
  "✅ Harmless Module."
).add()
