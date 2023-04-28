import discord
import tempfile
import os

import random
import itertools

from utils import moviepy_utils



intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

TOKEN = os.getenv("DISCORD_SOJUBOT_TOKEN")
HISTORY_LIMIT = 200










def get_file_type(our_file):
    extension = our_file.split(".")[-1]
    return "." + extension
    











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











def get_media_input_urls(inputs= []):
    img = []
    aud = []
    vid = []

    for input in inputs:
        if is_vid(input):
            embeded = getattr(getattr(input, "video", None), "url", None)
            attached = getattr(input, "url", None)
            right_one = attached if embeded == None else embeded
            vid.append(right_one)        

        elif is_aud(input):
            aud.append(getattr(input, "url", None))

        elif is_img(input):
            embeded = getattr(getattr(input, "image", None), "url", None)
            attached = getattr(input, "url", None)
            right_one = attached if embeded == None else embeded
            img.append(right_one)

    return (img, aud, vid)













async def get_main_input_from_reference(message= None, allow_audio= False):
    if not message:
        return None
     
    embeds_list = [m for m in list(message.embeds)]
    attachs_list = [m for m in list(message.attachments)]

    img, aud, vid = get_media_input_urls(embeds_list + attachs_list)

    backup = random.choice(aud) if allow_audio and len(aud) > 0 else None

    return random.choice(vid) if len(vid) > 0 else backup












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
    aux_img, aux_aud, aux_vid = get_media_input_urls(embeds)
    img = img + aux_img
    aud = aud + aux_aud
    vid = vid + aux_vid


    attachs = [m for m in list(itertools.chain(*attachs_lists))]
    aux_img, aux_aud, aux_vid = get_media_input_urls(attachs)
    img = img + aux_img
    aud = aud + aux_aud
    vid = vid + aux_vid
 
    vid.remove(main_input) if main_input in vid else None

    return img, aud, vid






async def make_it_goofy(message= None, tmp_dir= "./"):
    feedback_msg = "hueuehuehuheuhe"
    outfilename = "hahhaha.mp3"


    return { "feedback": feedback_msg,  "goofyedit": outfilename}











async def build_soju_file(message= None, tmp_dir= "./"):
    feedback_msg = ""
    outfilename = ""

    if (
        message
        and message.reference
        and message.reference.message_id != None
    ):
        main_msg = await message.channel.fetch_message(message.reference.message_id)
        ffmpeg_main_input = await get_main_input_from_reference(main_msg, allow_audio= True)

        if (ffmpeg_main_input != None):

            img, aud, vid = await get_random_media_inputs(message, ffmpeg_main_input) 

            try:
                outfilename = await moviepy_utils.buildSojuFileAsync(
                    videofilepath= ffmpeg_main_input,
                    random_media= (img, aud, vid),
                    tmp_dir= tmp_dir
                )
                feedback_msg = f"Someone ( 🤖 or something) might have slid into ur DMs... 🤨 👀 🛝"

            except FileNotFoundError:
                feedback_msg = f"Apparently the file referenced has no audio 🔊 streams\ntherefore 🧐 It can't have it's audio described"

            except Exception as e:
                # feedback_msg = f"I'm afraid Soju can't describe {get_file_type(ffmpeg_main_input)} files 😅"
                feedback_msg = f"error 💀\n> {e}"
        else:
            feedback_msg = "no valid files were found for audio description 🗿🗿🗿"

    return { "feedback": feedback_msg, "sojufile": outfilename }









async def edit_video_file(message= None):
    return "edit_video_call"




def is_describe_audio_call(message):

    if (
        message.reference
        and not message.attachments
    ):
        return True
    else:
        return False
    





def is_video_edit_call(message):

    if (
        message.reference
        and message.attachments
    ):
        return True
    else:
        return False    










@client.event
async def on_ready():

    print(f'We have logged in as {client.user}')




@client.event
async def on_message(message) :

    if message.author == client.user :
        return
    
    if message.content.startswith('!soju') :

        if is_describe_audio_call(message) :
            with tempfile.TemporaryDirectory(dir="./") as tmp_dir:
                ephemeral = tmp_dir + "/"
                dict_ = await build_soju_file(message, ephemeral)
                if dict_["sojufile"] :
                    await message.author.send(file= discord.File(ephemeral + dict_["sojufile"]))

            feedback_msg = dict_["feedback"]
            await message.channel.send(feedback_msg, reference= message)


        elif is_video_edit_call(message) :
            with tempfile.TemporaryDirectory(dir="./") as tmp_dir:
                ephemeral = tmp_dir + "/"
                dict_ = await make_it_goofy(message, ephemeral)
                if dict_["goofyedit"] :
                    await message.author.send(file= discord.File(ephemeral + dict_["goofyedit"]))

            feedback_msg = dict_["feedback"]
            await message.channel.send(feedback_msg, reference= message)


        else :
            feedback_msg = "Soju's here to help u make some goofy ahh edits 🤓👍\nCheck out my documentation at 🔥 http://bointuber.netlify.app 🔥"
            await message.channel.send(feedback_msg, reference= message)


client.run(TOKEN)