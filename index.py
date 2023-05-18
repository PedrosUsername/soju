import discord
import tempfile
import requests
import os

import random
import itertools

from utils import moviepy_utils, ffmpeg_utils, vosk_utils, boomer_utils as bu



intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

TOKEN = os.getenv("DISCORD_SOJUBOT_TOKEN")




HISTORY_LIMIT = 200
TMP_AUDIO_FILE_NAME = "tmp_audio.wav"
SOJUCALL = "!soju"








def get_file_type(our_file):
    extension = our_file.split(".")[-1]
    return "." + extension
    






def download_file_from_url(link, response_path= "./"): 
       
    # create response object 
    r = requests.get(link, stream = True) 
        
    # download started 
    with open(response_path, 'wb') as f: 
        for chunk in r.iter_content(chunk_size = 1024*1024): 
            if chunk: 
                f.write(chunk)




def is_img(input= None) :
    if input == None:
        return False
    
    attr_type = getattr(input, "type", getattr(input, "content_type", None))

    if (
        attr_type != None
        and ("image" in attr_type or "gifv" in attr_type)
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
        and "video" in attr_type
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













async def get_main_clip_url_from_referenced_message(message= None, allow_audio= False):
    if not message:
        return None
    
    referenced_message = await message.channel.fetch_message(message.reference.message_id)

    embeds_list = [m for m in list(referenced_message.embeds)]
    attachs_list = [m for m in list(referenced_message.attachments)]

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
        main_input_url = await get_main_clip_url_from_referenced_message(message, allow_audio= True)
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





















def is_describe_audio_call(message= None, sojufile= None) :
    if (
        message is None
        or message.reference is None
        or message.reference.message_id is None
    ) :
        return False
    
    issojucall = message.content.startswith('!soju')
    b_gen = bu.get_boomer_generator_from_dict(sojufile)

    if issojucall or b_gen :
        return True
    
    else:
        return False
    



def is_video_edit_call(message= None, sojufile= None) :
    if (
        message is None
        or message.reference is None
        or message.reference.message_id is None
        or message.attachments is None
    ) :
        return False
    
    boomers = bu.get_boomers_from_dict(sojufile)
    b_gen = bu.get_boomer_generator_from_dict(sojufile)

    if (
        boomers is not None
        and b_gen is None
    ) :
        return True
    
    else :
        return False



def is_credits_call(message) :
    if (
        message is None
    ) :
        return False
    
    issojucall = message.content.startswith(SOJUCALL)

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

        sojufile = bu.get_sojufile_from_url_as_dict(await get_soju_file(message))


        if is_describe_audio_call(message, sojufile) :
            await message.channel.send("wait a second...", reference= message)
            feedback_msg = "have fun!"
            brand_new_file = None

            with tempfile.TemporaryDirectory(dir="./") as tmp_dir :
                ephemeral = tmp_dir + "/"
                main_clip_url = await get_main_clip_url_from_referenced_message(message, allow_audio= True)                    

                #try :
                main_clip_name = moviepy_utils.get_base_file_name_from(main_clip_url)
                
                if main_clip_url is None :
                    raise Exception("clip not found")

                full_main_clip_file_path = ephemeral + main_clip_name + ".mp4"
                full_aux_audio_file_path = ephemeral + main_clip_name + ".wav"
                full_new_soju_file_path = ephemeral + main_clip_name + ".soju.json"            

                download_file_from_url(main_clip_url, full_main_clip_file_path)                        
                ffmpeg_utils.get_only_audio(full_main_clip_file_path, full_aux_audio_file_path)

                moviepy_utils.init_og_clip_params(full_main_clip_file_path)

                boomers = vosk_utils.describe(
                    audio_file_path= full_aux_audio_file_path,
                    generator= bu.get_boomer_generator_from_dict(sojufile)
                )

                bu.build_sojufile_for_discord(full_new_soju_file_path, boomers)
                brand_new_file = discord.File(full_new_soju_file_path)
                #except Exception as err :
                #    feedback_msg = f"💀 Audio Description Error"

                await message.author.send(feedback_msg, file= brand_new_file)







        elif is_video_edit_call(message, sojufile) :
            await message.channel.send("wait a moment...", reference= message)
            feedback_msg = "done!"
            brand_new_video = None

            with tempfile.TemporaryDirectory(dir="./") as tmp_dir :
                ephemeral = tmp_dir + "/"
                main_clip_url = await get_main_clip_url_from_referenced_message(message, allow_audio= True)

                try :
                    boomers = bu.get_boomers_from_dict(sojufile)
                    main_clip_name = moviepy_utils.get_base_file_name_from(main_clip_url)

                    if len(boomers) < 1 :
                        raise Exception("boomers list is empty")

                    if main_clip_url is None :
                        raise Exception("clip not found")
                    

                    full_main_clip_file_path = ephemeral + main_clip_name + ".mp4"
                    full_main_clip_file_path_copy = ephemeral + main_clip_name + "_copy.mp4"

                    download_file_from_url(main_clip_url, full_main_clip_file_path_copy)                        

                    moviepy_utils.init_og_clip_params(full_main_clip_file_path_copy)

                    boomers_top, boomers_mid, boomers_bot = bu.filterBoomers(
                        og_clip_duration= moviepy_utils.get_og_clip_params().get("duration"),
                        boomers= boomers
                    )

                    params = ffmpeg_utils.buildCall(
                        full_main_clip_file_path,
                        boomers_top,
                        boomers_mid,
                        boomers_bot
                    )

                    for p in params :
                        print(p, end= "\n\n")

                    ffmpeg_utils.executeFfmpegCall(
                        params= params
                    )
                    brand_new_video = discord.File(full_main_clip_file_path)
                except Exception as err :
                    feedback_msg = f"💀 Video Edition Error:\n\n👉 {err}"

                await message.author.send(feedback_msg, file= brand_new_video)





        elif is_credits_call(message) :
            feedback_msg = "Soju's here to help u make some goofy ahh edits 🤓👍\nCheck out my documentation at 🔥 http://github.com/pedrosusername 🔥"
            await message.channel.send(feedback_msg, reference= message)            


client.run(TOKEN)





# issue 0000 > server straight up freezes with certain http input requests
# issue 0001 > soju videos encoding aren't suitable for youtube or twitter upload. They need to be "converted to mp4" before.