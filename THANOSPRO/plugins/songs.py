import asyncio
import time

from telethon.tl.types import DocumentAttributeAudio
from yt_dlp import YoutubeDL
from yt_dlp.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import *


@rishu_cmd(pattern="song(?:\s|$)([\s\S]*)")
async def _(event):
    xyz = await client_id(event)
    ultronceo, rishu_mention = xyz[0], xyz[2]
    query = event.text[6:]
    max_results = 1
    if query == "":
        return await eod(event, "__Please give a song name to search.__")
    rishu = await eor(event, f"__Searching for__ `{query}`")
    hel_ = await song_search(event, query, max_results, details=True)
    x, title, views, duration, thumb = hel_[0], hel_[1], hel_[2], hel_[3], hel_[4]
    thumb_name = f'thumb{ultronceo}.jpg'
    thumbnail = requests.get(thumb, allow_redirects=True)
    open(thumb_name, 'wb').write(thumbnail.content)
    url = x.replace("\n", "")
    try:
        await rishu.edit("**Fetching Song**")
        with YoutubeDL(song_opts) as somg:
            rishu_data = somg.extract_info(url)
    except DownloadError as DE:
        return await eod(rishu, f"`{str(DE)}`")
    except ContentTooShortError:
        return await eod(rishu, "`The download content was too short.`")
    except GeoRestrictedError:
        return await eod(rishu, "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`")
    except MaxDownloadsReached:
        return await eod(rishu, "`Max-downloads limit has been reached.`")
    except PostProcessingError:
        return await eod(rishu, "`There was an error during post processing.`")
    except UnavailableVideoError:
        return await eod(rishu, "`Media is not available in the requested format.`")
    except XAttrMetadataError as XAME:
        return await eod(rishu, f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        return await eod(rishu, "`There was an error during info extraction.`")
    except Exception as e:
        return await eod(rishu, f"{str(type(e)): {str(e)}}")
    c_time = time.time()
    await rishu.edit(f"**🎶 Preparing to upload song 🎶 :** \n\n{rishu_data['title']} \n**By :** {rishu_data['uploader']}")
    await event.client.send_file(
        event.chat_id,
        f"{rishu_data['id']}.mp3",
        supports_streaming=True,
        caption=f"**✘ Song -** `{title}` \n**✘ Views -** `{views}` \n**✘ Duration -** `{duration}` \n\n**✘ By :** {rishu_mention}",
        thumb=thumb_name,
        attributes=[
            DocumentAttributeAudio(
                duration=int(rishu_data["duration"]),
                title=str(rishu_data["title"]),
                performer=perf,
            )
        ],
        progress_callback=lambda d, t: asyncio.get_running_loop().create_task(
            progress(d, t, event, c_time, "Uploading..", f"{rishu_data['title']}.mp3")
        ),
    )
    await rishu.delete()
    os.remove(f"{rishu_data['id']}.mp3")


@rishu_cmd(pattern="vsong(?:\s|$)([\s\S]*)")
async def _(event):
    xyz = await client_id(event)
    ultronceo, rishu_mention = xyz[0], xyz[2]
    query = event.text[7:]
    max_results = 1
    if query == "":
        return await eod(event, "__Please give a song name to search.__")
    rishu = await eor(event, f"__Searching for__ `{query}`")
    hel_ = await song_search(event, query, max_results, details=True)
    x, title, views, duration, thumb = hel_[0], hel_[1], hel_[2], hel_[3], hel_[4]
    thumb_name = f'thumb{ultronceo}.jpg'
    thumbnail = requests.get(thumb, allow_redirects=True)
    open(thumb_name, 'wb').write(thumbnail.content)
    url = x.replace("\n", "")
    try:
        await rishu.edit("**Fetching Video**")
        with YoutubeDL(video_opts) as somg:
            rishu_data = somg.extract_info(url)
    except DownloadError as DE:
        return await eod(rishu, f"`{str(DE)}`")
    except ContentTooShortError:
        return await eod(rishu, "`The download content was too short.`")
    except GeoRestrictedError:
        return await eod(rishu, "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`")
    except MaxDownloadsReached:
        return await eod(rishu, "`Max-downloads limit has been reached.`")
    except PostProcessingError:
        return await eod(rishu, "`There was an error during post processing.`")
    except UnavailableVideoError:
        return await eod(rishu, "`Media is not available in the requested format.`")
    except XAttrMetadataError as XAME:
        return await eod(rishu, f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        return await eod(rishu, "`There was an error during info extraction.`")
    except Exception as e:
        return await eod(rishu, f"{str(type(e)): {str(e)}}")
    c_time = time.time()
    await rishu.edit(f"**📺 Preparing to upload video 📺 :** \n\n{rishu_data['title']}\n**By :** {rishu_data['uploader']}")
    await event.client.send_file(
        event.chat_id,
        f"{rishu_data['id']}.mp4",
        supports_streaming=True,
        caption=f"**✘ Video :** `{title}` \n\n**✘ By :** {rishu_mention}",
        thumb=thumb_name,
        progress_callback=lambda d, t: asyncio.get_running_loop().create_task(
            progress(d, t, event, c_time, "Uploading..", f"{rishu_data['title']}.mp4")
        ),
    )
    await rishu.delete()
    os.remove(f"{rishu_data['id']}.mp4")


@rishu_cmd(pattern="lyrics(?: |$)(.*)")
async def nope(kraken):
    rishu = kraken.text[8:]
    uwu = await eor(kraken, f"Searching lyrics for  `{rishu}` ...")
    if not rishu:
        if kraken.is_reply:
            (await kraken.get_reply_message()).message
        else:
            await eod(uwu, "Give song name to get lyrics...")
            return
    try:
        troll = await event.client.inline_query("iLyricsBot", f"{(deEmojify(rishu))}")
        owo = await troll[0].click(Config.LOGGER_ID)
        await asyncio.sleep(3)
        owo_id = owo.id
        lyri = await event.client.get_messages(entity=Config.LOGGER_ID, ids=owo_id)
        await event.client.send_message(kraken.chat_id, lyri)
        await uwu.delete()
        await owo.delete()
    except Exception as e:
        await uwu.edir(f"**ERROR !!** \n\n`{str(e)}`")


@rishu_cmd(pattern="lsong(?:\s|$)([\s\S]*)")
async def _(event):
    rishu_ = event.text[6:]
    xyz = await client_id(event)
    ultronceo, rishu_mention = xyz[0], xyz[2]
    if rishu_ == "":
        return await eor(event, "Give a song name to search")
    rishu = await eor(event, f"Searching song `{rishu_}`")
    somg = await event.client.inline_query("Lybot", f"{(deEmojify(rishu_))}")
    if somg:
        fak = await somg[0].click(Config.LOGGER_ID)
        if fak:
            await event.client.send_file(
                event.chat_id,
                file=fak,
                caption=f"**Song by :** {rishu_mention}",
            )
        await rishu.delete()
        await fak.delete()
    else:
        await rishu.edit("**ERROR 404 :** __NOT FOUND__")


@rishu_cmd(pattern="wsong(?:\s|$)([\s\S]*)")
async def _(event):
    if not event.reply_to_msg_id:
        return await eor(event, "Reply to a mp3 file.")
    rply = await event.get_reply_message()
    chat = "@auddbot"
    rishu = await eor(event, "Trying to identify song...")
    async with event.client.conversation(chat) as conv:
        try:
            first = await conv.send_message("/start")
            second = await conv.get_response()
            third = await conv.send_message(rply)
            fourth = await conv.get_response()
            if not fourth.text.startswith("Audio received"):
                await rishu.edit(
                    "Error identifying audio."
                )
                await event.client.delete_messages(conv.chat_id, [first.id, second.id, third.id, fourth.id])
                return
            await rishu.edit("Processed...")
            fifth = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await rishu.edit("Please unblock @auddbot and try again")
    audio = f"**Song Name : **{fifth.text.splitlines()[0]}\n\n**Details : **__{fifth.text.splitlines()[2]}__"
    await rishu.edit(audio)
    await event.client.delete_messages(conv.chat_id, [first.id, second.id, third.id, fourth.id, fifth.id])


@rishu_cmd(pattern="spotify(?:\s|$)([\s\S]*)")
async def _(event):
    text = event.text[9:]
    chat = "@spotifysavebot"
    if text == "":
        return await eod(event, "Give something to download from Spotify.")
    rishu = await eor(event, f"**Trying to download** `{text}` **from Spotify...**")
    async with event.client.conversation(chat) as conv:
        try:
            first = await conv.send_message("/start")
            second = await conv.get_response()
            somg = await event.client.inline_query("spotifysavebot", f"str: {(deEmojify(text))}")
            if somg:
                third = await somg[0].click(chat)
            else:
                return await eod(rishu, "**ERROR !!** __404 : NOT FOUND__")
            fourth = await conv.get_response()
            fifth = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await eod(rishu, f"Please unblock {chat} to use Spotify module.")
        except Exception as e:
            return await eod(rishu, f"**ERROR !!** \n\n{e}")
        await event.client.send_file(event.chat_id, file=fourth, caption="")
        await rishu.delete()
        await event.client.delete_messages(conv.chat_id, [first.id, second.id, third.id, fourth.id, fifth.id])


CmdHelp("songs").add_command(
  "song", "<song name>", "Downloads the song from YouTube."
).add_command(
  "vsong", "<song name>", "Downloads the Video Song from YouTube."
).add_command(
  "lsong", "<song name>", "Sends the searched song in current chat.", "lsong Alone"
).add_command(
  "wsong", "<reply to a song file>", "Searches for the details of replied mp3 song file and uploads it's details."
).add_command(
  "lyrics", "<song name>", "Gives the lyrics of that song.."
).add_command(
  "spotify", "<song name>", "Downloads the song from Spotify."
).add_info(
  "Songs & Lyrics."
).add_warning(
  "✅ Harmless Module."
).add()
