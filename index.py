import discord
import tempfile
import os

import random
import itertools

from utils import moviepy_utils


TOKEN = os.getenv("DISCORD_SOJUBOT_TOKEN")

HISTORY_LIMIT = 200




def is_img(input= None):
    if input == None:
        return False
    
    if "image" in getattr(input, "type", getattr(input, "content_type", "")):
        return True
    else:
        return False
    



def is_aud(input= None):
    if input == None:
        return False
    
    if "audio" in getattr(input, "type", getattr(input, "content_type", "")):
        return True
    else:
        return False




def is_vid(input= None):
    if input == None:
        return False
    
    if (
        "video" in getattr(input, "type", getattr(input, "content_type", ""))
        or "gifv" in getattr(input, "type", getattr(input, "content_type", ""))
    ):
        return True
    else:
        return False        




def classify_media_inputs(inputs= []):
    img = []
    aud = []
    vid = []

    for input in inputs:
        if is_img(input):
            embeded = getattr(getattr(input, "image", None), "url", None)
            attached = getattr(input, "url", None)
            right_one = attached if embeded == None else embeded
            img.append(right_one)
        if is_aud(input):
            aud.append(getattr(input, "url", None))
        if is_vid(input):
            embeded = getattr(getattr(input, "video", None), "url", None)
            attached = getattr(input, "url", None)
            right_one = attached if embeded == None else embeded
            vid.append(right_one)

    return (img, aud, vid)


async def get_media_from_reference(message= None):
    if not message:
        return None
     
    embed_urls = [m.url for m in list(message.embeds)]
    attach_urls = [m.url for m in list(message.attachments)]

    media = attach_urls + embed_urls

    return media[0] if len(media) > 0 else None


async def get_random_media_inputs(message= None, main_input= None):
    if not message:
        return ""
    
    msgs = [message async for message in message.channel.history(limit=HISTORY_LIMIT)]

    random.shuffle(msgs)

    embeds_lists = [msg.embeds for msg in msgs]
    attachs_lists = [msg.attachments for msg in msgs]
    
    img = []
    aud = []
    vid = []

    embeds = [m for m in list(itertools.chain(*embeds_lists))]
    aux_img, aux_aud, aux_vid = classify_media_inputs(embeds)
    img = img + aux_img
    aud = aud + aux_aud
    vid = vid + aux_vid


    attachs = [m for m in list(itertools.chain(*attachs_lists))]
    aux_img, aux_aud, aux_vid = classify_media_inputs(attachs)
    img = img + aux_img
    aud = aud + aux_aud
    vid = vid + aux_vid
 
    vid.remove(main_input) if main_input in vid else None

    return img, aud, vid







intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if (message.content.startswith('soju')):
        ffmpeg_main_input, img, aud, vid = None, None, None, None
        
        if (message.reference != None and message.reference.message_id != None):
            main_msg = await message.channel.fetch_message(message.reference.message_id)
            ffmpeg_main_input = await get_media_from_reference(main_msg)

            if (ffmpeg_main_input != None):
                img, aud, vid = await get_random_media_inputs(message, ffmpeg_main_input) 

            with tempfile.TemporaryDirectory(dir="./") as tmp_dir:
                ephemeral = tmp_dir + "/"
                outfilename = await moviepy_utils.buildSojuFileAsync(videofilepath= ffmpeg_main_input, tmp_dir= ephemeral)
                await message.author.send(file= discord.File(tmp_dir + "/" + outfilename))

client.run(TOKEN)