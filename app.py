import os
import random
import requests
import tempfile

from utils import boomer_utils as bu
import utils.cli as soju

from interactions import Client, ContextMenuContext, File, listen, message_context_menu



bot = Client(
  token= os.getenv("DISCORD_SOJUBOT_TOKEN"),
  delete_unused_application_cmds= True
)








def get_base_file_name_from(videofilepath= None) :
    if videofilepath is None :
        return None
    
    filename = os.path.basename(videofilepath)
    _, tail = filename[::-1].split(".", 1)
    return tail[::-1]



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



async def get_main_clip_url_from_referenced_message(referenced_message= None, allow_audio= False):
    if not referenced_message:
        return None
    
    # embeds_list = [m for m in list(referenced_message.embeds)]
    attachs_list = [m for m in list(referenced_message.attachments)]

    img, aud, vid = get_media_input_urls(attachs_list)

    backup = random.choice(aud) if allow_audio and len(aud) > 0 else None

    return random.choice(vid) if len(vid) > 0 else backup





MAKEITREAL_GENERATOR_PATH = "./assets/json/makeitreal.soju.json"


async def edit(params= {}) :
    videofilepath = params.get("clip") if params.get("clip") else None
    jsonfilepath = params.get("json") if params.get("json") else MAKEITREAL_GENERATOR_PATH
    dropzone = params.get("outputpath") if params.get("outputpath") else "./"

    sojufile= bu.get_sojufile_from_path(jsonfilepath)
    boomers = bu.get_boomers_from_dict(sojufile)
    generator = bu.prepare_boomer_generator(bu.get_boomer_generator_from_dict(sojufile))

    generator["generals"]["dropzone"] = dropzone

    print("wait a second...")
    await soju.audio_descriptor(videofilepath, generator)

    new_sojufile = soju.bu.get_sojufile_from_path(dropzone + soju.file_utils.get_base_file_name_from(videofilepath) + ".soju.json")
    boomers = new_sojufile.get("generated") if new_sojufile.get("generated") else []

    print("wait a moment...")
    soju.video_editor(videofilepath, generator, boomers)










@listen()
async def on_startup():
    print("Bot is ready!")



@message_context_menu(
  name="make it real",
  scopes=[1100512333203259552]
)
async def prepare_and_edit(ctx: ContextMenuContext):
  await ctx.defer()
  clip_url = await get_main_clip_url_from_referenced_message(ctx.target)
  clip_title = get_base_file_name_from(clip_url)

  with tempfile.TemporaryDirectory(dir="./") as tmp_dir_upload :
    ephemeral_upload = tmp_dir_upload + "/"

    with tempfile.TemporaryDirectory(dir="./") as tmp_dir_download :
      ephemeral_download = tmp_dir_download + "/"

      clip_path_download = ephemeral_download + clip_title + ".mp4"
      outputpath = ephemeral_upload

      download_file_from_url(clip_url, clip_path_download)

      await edit({
          "clip": clip_path_download,
          "json": "./assets/json/makeitreal.soju.json",
          "outputpath": outputpath
      })

      await ctx.send(file= File(outputpath + clip_title + ".mp4"))



bot.start()








"""
import requests


get_local_comm = "https://discord.com/api/v10/applications/1100516866641891391/guilds/1100512333203259552/commands"
delete_local_comm = "https://discord.com/api/v10/applications/1100516866641891391/guilds/1100512333203259552/commands/1119884701646192660"
create_local_comm = "https://discord.com/api/v10/applications/1100516866641891391/guilds/1100512333203259552/commands"

# This is an example USER command, with a type of 2
json = {
    "name": "Make it Red",d
    "type": 3
}

# For authorization, you can use either your bot token
headers = {
    "Authorization": "Bot MTEwMDUxNjg2NjY0MTg5MTM5MQ.G62Emz.tzG3c613Nn7H3HZuO3_h53UZvPWf-93M6myfkU"
}


r = requests.delete(delete_local_comm, headers=headers)

print(r.text)
"""