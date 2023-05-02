import discord
import tempfile
import json
import os

import random
import itertools

from utils import moviepy_utils, ffmpeg_utils, boomer_utils as bu



intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

TOKEN = os.getenv("DISCORD_SOJUBOT_TOKEN")




HISTORY_LIMIT = 200










def get_file_type(our_file):
    extension = our_file.split(".")[-1]
    return "." + extension
    











def is_img(input= None) :
    if input == None:
        return False
    
    attr_type = getattr(input, "type", getattr(input, "content_type", None))

    if (
        attr_type != None
        and "image" in attr_type
    ) :
        return True
    else:
        return False
    



def is_aud(input= None) :
    if input == None:
        return False
    
    attr_type = getattr(input, "type", getattr(input, "content_type", None))

    if (
        attr_type != None
        and "audio" in attr_type
    ) :
        return True
    else:
        return False




def is_vid(input= None) :
    if input == None:
        return False
    
    attr_type = getattr(input, "type", getattr(input, "content_type", None))

    if (
        attr_type != None
        and ("video" in attr_type or "gifv" in attr_type)
    ) :
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













async def get_main_input_from_message(message= None, allow_audio= False):
    if not message:
        return None
     
    embeds_list = [m for m in list(message.embeds)]
    attachs_list = [m for m in list(message.attachments)]

    img, aud, vid = get_media_input_urls(embeds_list + attachs_list)

    backup = random.choice(aud) if allow_audio and len(aud) > 0 else None

    return random.choice(vid) if len(vid) > 0 else backup







async def get_soju_file(message= None) :
    if message is None or message.attachments is None :
        return None
    
    json_files = [ attachment.url for attachment in message.attachments if get_file_type(attachment.url) == '.json']

    return random.choice(json_files) if len(json_files) > 0 else None












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






async def make_it_goofy(message= None, tmp_dir= "./", sojufile= None) :
    feedback_msg = None
    outfilename = None

    if (
        message
        and message.reference
        and message.reference.message_id != None
    ) :
        referenced_message = await message.channel.fetch_message(message.reference.message_id)

        main_input_url = await get_main_input_from_message(referenced_message, allow_audio= True)

        ffmpeg_copy_output = tmp_dir + "moviepy_friendly_copy.mp4"

        if (main_input_url != None and sojufile != None) :
            ffmpeg_utils.copy(from_= main_input_url, to_= ffmpeg_copy_output)
            outfilename = moviepy_utils.makeItGoofyForDiscord(
                moviepycopy= ffmpeg_copy_output,
                main_input_url= main_input_url,
                sojufile= sojufile,
                tmp_dir= tmp_dir
            )    


            feedback_msg = "done 👍"            
        else :
            feedback_msg = "sorry, not enough valid input files"
    else :
        feedback_msg = "runtime error 💀"


    return { "feedback": feedback_msg,  "file": outfilename }











async def build_soju_file(message= None, tmp_dir= "./", sojufile= None) :
    feedback_msg = None
    outfilename = None

    if (
        message
        and message.reference
        and message.reference.message_id != None
    ):
        main_msg = await message.channel.fetch_message(message.reference.message_id)
        ffmpeg_main_input = await get_main_input_from_message(main_msg, allow_audio= True)

        if (ffmpeg_main_input != None) :

            img, aud, vid = await get_random_media_inputs(message, ffmpeg_main_input) 

            outfilename = moviepy_utils.buildSojuFileForDiscord(
                videofilepath= ffmpeg_main_input,
                sojufile= sojufile,
                random_media= (img, aud, vid),
                tmp_dir= tmp_dir
            )


            feedback_msg = "done 👍"
        else :
            feedback_msg = "sorry, not enough valid input files"
    else :
        feedback_msg = "run time error 💀"


    return { "feedback": feedback_msg, "file": outfilename }












async def is_describe_audio_call(message, sojufile= None) :
    if (
        not message
        or not message.reference
    ) :
        return False
    
    issojucall = message.content.startswith('!soju')
    b_gen = bu.get_boomer_generator_from_dict(sojufile)

    if issojucall or b_gen :
        return True
    
    else:
        return False
    





async def is_video_edit_call(message= None, sojufile= None) :
    if (
        not message
        or not message.reference
        or not message.attachments
    ) :
        return False

    boomers = bu.get_boomers_from_dict(sojufile)
    b_gen = bu.get_boomer_generator_from_dict(sojufile)

    if len(boomers) > 0 and b_gen is None :
        return True
    else :
        return False



def is_credits_call(message) :
    if (
        not message
    ) :
        return False
    
    issojucall = message.content.startswith('!soju')

    if issojucall :
        return True
    
    else:
        return False

















@client.event
async def on_ready() :

    print(f'We have logged in as {client.user}')




@client.event
async def on_message(message) :

    if message.author == client.user :
        return
    
    elif message.channel.guild != None :

        sojufile = bu.get_sojufile_confs_from_url(await get_soju_file(message))

        if await is_describe_audio_call(message, sojufile) :
            await message.channel.send("wait a second...", reference= message)

            with tempfile.TemporaryDirectory(dir="./") as tmp_dir :
                ephemeral = tmp_dir + "/"
                try :
                    dict_ = await build_soju_file(message, ephemeral, sojufile)

                    if dict_["file"] :
                        await message.author.send(file= discord.File(dict_["file"]))
                        feedback_msg = dict_["feedback"]                    
                    else :
                        feedback_msg = "🗿 Soju tried to build a soju.file for you, 📂 but no valid references were found for that 🗿🗿"
                        
                except FileNotFoundError:
                    feedback_msg = f"FileNotFound exception 🔥\nApparently the file you referenced has no audio 🔊 streams 🧐\nbut it could be something else 👍👌"
            
                except discord.HTTPException:
                    feedback_msg = "HTTPException: Even tho discord's standard limit for file size is 25MB, the API still limits soju to 8MB only"

                except Exception as err:
                    feedback_msg = f"Error 💀\n> {err}"

            await message.channel.send(feedback_msg, reference= message)





        elif await is_video_edit_call(message, sojufile) :
            await message.channel.send("wait a second...", reference= message)

            with tempfile.TemporaryDirectory(dir="./") as tmp_dir :
                ephemeral = tmp_dir + "/"
                try :
                    dict_ = await make_it_goofy(message, ephemeral, sojufile)

                    if dict_["file"] :
                            await message.author.send(file= discord.File(dict_["file"]))
                            feedback_msg = dict_["feedback"]
                    else :
                        feedback_msg = "🗿🗿 Soju tried to make a goofy edition, but couldn't with 📂 files you provided 🗿"

                except FileNotFoundError :
                    feedback_msg = f"FileNotFound exception 💀\nApparently the file you referenced has no audio 🔊 streams 🧐\nbut it could be something else 👌👍"
        
                except KeyError as err :
                    if "video" in str(err) :
                        feedback_msg = f"💀 We got a KeyError exception 🔥\nWe may have a problem with the video stream of the file you referenced 🧐\nbut it could be something else 👌👍"
                    else :
                        feedback_msg = "💀 We got a KeyError exception 🔥\nSoju could not process the file you referenced..."

                except ValueError as err :
                    feedback_msg = f"We got a ValueException 💀💀\nThe json file provided might have invalid json\nbut it could be something else 👍👌"
                
                except discord.HTTPException:
                    feedback_msg = "HTTPException: Sorry, even tho discord's standard limit for file size is 25MB, the API still limits soju to 8MB only\nSoju can't send files bigger than 8mb. Try referencing 30 second videos at best."

                except Exception as err:
                    feedback_msg = f"Error 💀\nI have no idea what happened lol 😂😂\n> {err}"

            await message.channel.send(feedback_msg, reference= message)


        elif is_credits_call(message) :
            feedback_msg = "Soju's here to help u make some goofy ahh edits 🤓👍\nCheck out my documentation at 🔥 http://bointuber.netlify.app 🔥"
            await message.channel.send(feedback_msg, reference= message)            


client.run(TOKEN)