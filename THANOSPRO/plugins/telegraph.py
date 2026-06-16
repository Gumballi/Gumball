import os
import datetime

from PIL import Image
from telegraph import Telegraph, exceptions, upload_file

from . import *


@rishu_cmd(pattern="t(m|t)(?:\s|$)([\s\S]*)")
async def telegraph_handler(event):
    if Config.LOGGER_ID is None:
        await eod(event, "You need to setup `LOGGER_ID` to use telegraph...")
        return
        
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
        
    telegraph = Telegraph()
    telegraph.create_account(short_name="THANOSPRO")
    
    input_type = event.pattern_match.group(1)
    optional_title = event.pattern_match.group(2).strip()
    
    rishu = await eor(event, "Processing Telegraph request...")
    cids = await client_id(event)
    rishu_mention = cids[2]
    
    if not event.reply_to_msg_id:
        return await eod(rishu, "Reply to a message to get a permanent telegra.ph link.")
        
    start = datetime.datetime.now()
    r_message = await event.get_reply_message()
    
    if input_type == "m":
        # Media to Telegraph
        if not r_message.media:
            return await eod(rishu, "Reply to a media message with `.tm`")
            
        downloaded_file_name = await event.client.download_media(
            r_message, Config.TMP_DOWNLOAD_DIRECTORY
        )
        
        if not downloaded_file_name:
            return await eod(rishu, "Failed to download media.")
            
        await rishu.edit(f"Downloaded to `{os.path.basename(downloaded_file_name)}`. Uploading...")
        
        if downloaded_file_name.endswith((".webp")):
            resize_image(downloaded_file_name)
            
        try:
            media_urls = upload_file(downloaded_file_name)
            end = datetime.datetime.now()
            ms = (end - start).seconds
            
            await rishu.edit(
                "✓ **[File uploaded to telegraph](https://telegra.ph{})**\n"
                "✓ **Time Taken :-** `{}` secs\n"
                "✓ **By :- {}**\n"
                "✓ `https://telegra.ph{}`".format(
                    media_urls[0], ms, rishu_mention, media_urls[0]
                ),
                link_preview=True,
            )
        except exceptions.TelegraphException as exc:
            await eod(rishu, "ERROR: " + str(exc), 8)
        finally:
            if os.path.exists(downloaded_file_name):
                os.remove(downloaded_file_name)
                
    elif input_type == "t":
        # Text to Telegraph
        title_of_page = optional_title or "THANOSPRO Paste"
        page_content = r_message.message or ""
        
        if r_message.media:
            downloaded_file_name = await event.client.download_media(
                r_message, Config.TMP_DOWNLOAD_DIRECTORY
            )
            if downloaded_file_name:
                try:
                    with open(downloaded_file_name, "rb") as fd:
                        content = fd.read().decode("UTF-8", errors="ignore")
                        page_content += "\n" + content
                except:
                    pass
                finally:
                    os.remove(downloaded_file_name)
        
        if not page_content.strip():
            return await eod(rishu, "No text content found to paste.")
            
        page_content = page_content.replace("\n", "<br>")
        
        try:
            response = telegraph.create_page(title_of_page, html_content=page_content)
            end = datetime.datetime.now()
            ms = (end - start).seconds
            url = f"https://telegra.ph/{response['path']}"
            await rishu.edit(
                f"✓ **[Pasted to telegraph]({url})**\n"
                f"✓ **Time Taken :-** `{ms}` secs\n"
                f"✓ **By :** {rishu_mention}\n"
                f"✓ `{url}`", 
                link_preview=True
            )
        except Exception as e:
            await eod(rishu, f"Error: `{str(e)}`")


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


CmdHelp("telegraph").add_command(
  "tt", "<reply to text message>", "Uploads the replied text message to telegraph making a short telegraph link"
).add_command(
  "tm", "<reply to media>", "Uploads the replied media (sticker/ gif/ video/ image) to telegraph and gives a short telegraph link"
).add_info(
  "Make Telegraph Links."
).add_warning(
  "✅ Harmless Module."
).add()
