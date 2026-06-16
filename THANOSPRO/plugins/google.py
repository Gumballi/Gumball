import asyncio
import datetime
import os
import requests

from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from search_engine_parser import GoogleSearch
from search_engine_parser.core.exceptions import NoResultsOrTrafficError as GoglError
from shutil import rmtree
from telethon.tl import types
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError

# Note: google_images_download is often broken due to Google's UI changes.
# We'll try to import it safely.
try:
    from google_images_download import google_images_download
except ImportError:
    google_images_download = None

from . import *

@rishu_cmd(pattern="wiki(?:\s|$)([\s\S]*)")
async def _(event):
    match = event.pattern_match.group(1).strip()
    if not match:
        return await eod(event, "`Give something to search on Wikipedia..`")
    
    result = None
    try:
        result = summary(match, auto_suggest=False)
    except DisambiguationError as error:
        error_lines = str(error).split("\n")
        result = "".join(
            f"`{i}`\n" if lineno > 1 else f"**{i}**\n"
            for lineno, i in enumerate(error_lines, start=1)
        )
        return await eor(event, f"**DISAMBIGUATED PAGE !!.**\n\n{result}")
    except PageError:
        pass
    
    if not result:
        try:
            result = summary(match, auto_suggest=True)
        except DisambiguationError as error:
            error_lines = str(error).split("\n")
            result = "".join(
                f"`{i}`\n" if lineno > 1 else f"**{i}**\n"
                for lineno, i in enumerate(error_lines, start=1)
            )
            return await eor(event, f"**DISAMBIGUATED PAGE !!**\n\n{result}")
        except PageError:
            return await eod(event, f"**Sorry i Can't find any results for **`{match}`")
            
    await eor(event, f"**Search :**\n`{match}`\n\n**Result:**\n__{result}__")


@rishu_cmd(pattern="google(?:\s|$)([\s\S]*)")
async def google(event):
    input_str = event.pattern_match.group(1).strip()
    if not input_str:
        return await eod(event, "`Give something to search..`")
    rishu = await eor(event, "Searching...")
    gos = GoogleSearch()
    try:
        got = await gos.async_search(f"{input_str}", cache=False)
    except GoglError as e:
        return await eod(event, str(e), 10)
    
    output = ""
    for i in range(len(got["links"])):
        text = got["titles"][i]
        url = got["links"][i]
        des = got["descriptions"][i]
        output += f"<a href='{url}'>• {text}</a>\n≈ <code>{des}</code>\n\n"
        
    res = f"""<h3><b><i>Google Search Query :</b></i> <u>{input_str}</u></h3>
»» <b>Results :</b>
{output}"""
    paste = await telegraph_paste(f"Google Search Query “ {input_str} ”", res)
    await rishu.edit(f"**Google Search For** `{input_str}` \n[📌 See Results Here]({paste})", link_preview=False)


@rishu_cmd(pattern="img(?:\s|$)([\s\S]*)")
async def img_search(event):
    if google_images_download is None:
        return await eod(event, "`google_images_download` library is not installed.")
        
    sim = event.pattern_match.group(1).strip()
    if not sim:
        return await eod(event, "`Give something to search...`")
        
    rishu = await eor(event, f"Searching for `{sim}`...")
    lim = 5
    if ";" in sim:
        try:
            parts = sim.split(";")
            sim = parts[0].strip()
            lim = int(parts[1].strip())
        except:
            pass
            
    response = google_images_download.googleimagesdownload()
    args = {
        "keywords": sim,
        "limit": lim,
        "format": "jpg",
        "output_directory": "./DOWNLOADS/",
    }
    
    try:
        paths = response.download(args)
        gotit = paths[0][sim]
        if gotit:
            await event.client.send_file(event.chat_id, gotit, caption=sim, album=True)
        else:
            await eod(rishu, "No images found.")
    except Exception as e:
        await eod(rishu, f"**Error:** `{str(e)}`")
    finally:
        if os.path.exists(f"./DOWNLOADS/{sim}/"):
            rmtree(f"./DOWNLOADS/{sim}/")
        await rishu.delete()


@rishu_cmd(pattern="reverse(?:\s|$)([\s\S]*)")
async def reverse_search(event):
    reply = await event.get_reply_message()
    if not reply:
        return await eod(event, "`Reply to an Image or sticker...`")
    
    rishu = await eor(event, "`Processing...`")
    dl = await reply.download_media()
    
    try:
        with open(dl, "rb") as f:
            file = {"encoded_image": (dl, f)}
            grs = requests.post(
                "https://www.google.com/searchbyimage/upload",
                files=file,
                allow_redirects=False,
            )
        
        loc = grs.headers.get("Location")
        if not loc:
            return await eod(rishu, "Google did not return a search location.")
            
        response = requests.get(
            loc,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0",
            },
        )
        
        xx = BeautifulSoup(response.text, "html.parser")
        divs = xx.find_all("div", {"class": "r5a77d"})
        if not divs:
            return await eod(rishu, "No possible results found on Google.")
            
        alls = divs[0].find("a")
        link = alls["href"]
        text = alls.text
        await rishu.edit(f"**Possible Results :** [{text}](https://google.com{link})")
        
        if google_images_download:
            img_downloader = google_images_download.googleimagesdownload()
            args = {
                "keywords": text,
                "limit": 3,
                "format": "jpg",
                "output_directory": "./DOWNLOADS/",
            }
            try:
                final = img_downloader.download(args)
                ok = final[0][text]
                if ok:
                    await event.client.send_file(
                        event.chat_id,
                        ok,
                        album=True,
                        caption=f"Similar Images Related to {text}",
                    )
            except:
                pass
            finally:
                if os.path.exists(f"./DOWNLOADS/{text}/"):
                    rmtree(f"./DOWNLOADS/{text}/")
    except Exception as e:
        await eod(rishu, f"**Error:** `{str(e)}`")
    finally:
        if os.path.exists(dl):
            os.remove(dl)


@rishu_cmd(pattern="gps(?:\s|$)([\s\S]*)")
async def gps_location(event):
    input_str = event.pattern_match.group(1).strip()
    if not input_str:
        return await eod(event, "What should i find? Give me location.🤨")
    
    rishu = await eor(event, "Finding😁")
    try:
        geolocator = Nominatim(user_agent="THANOSPRO")
        geoloc = geolocator.geocode(input_str)
        if geoloc:
            lon = geoloc.longitude
            lat = geoloc.latitude
            await event.respond(input_str, file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon)))
            await rishu.delete()
        else:
            await eod(rishu, "I couldn't find it😫")
    except Exception as e:
        await eod(rishu, f"**Error:** `{str(e)}`")


CmdHelp("google").add_command(
  "google", "<query>", "Does a google search for the query provided"
).add_command(
  "img", "<query>", "Does a image search for the query provided"
).add_command(
  "reverse", "<reply to a sticker/pic>", "Does a reverse image search on google and provides the similar images"
).add_command(
  "gps", "<place>", "Gives the location of the given place/city/state."
).add_command(
  "wiki", "<query>", "Searches for the query on Wikipedia."
).add_info(
  "Google Search."
).add_warning(
  "✅ Harmless Module."
).add()
