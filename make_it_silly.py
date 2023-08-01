import os
import tempfile
import random
import requests

from interactions import Client, ContextMenuContext, File, listen, message_context_menu, cooldown, Buckets
from utils import boomer_utils as bu, moviepy_utils as mu, cli as soju




HORIZONTAL_GENERATOR_PATH = "./assets/json/generator/make_it_silly/make_it_silly_h.soju.json"
VERTICAL_GENERATOR_PATH = "./assets/json/generator/make_it_silly/make_it_silly_v.soju.json"



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



def get_main_clip_url_from_referenced_message(referenced_message= None, allow_audio= False):
    if not referenced_message:
        return None
    
    # embeds_list = [m for m in list(referenced_message.embeds)]
    attachs_list = [m for m in list(referenced_message.attachments)]

    img, aud, vid = get_media_input_urls(attachs_list)

    backup = random.choice(aud) if allow_audio and len(aud) > 0 else None

    return random.choice(vid) if len(vid) > 0 else backup







async def edit(params= {}) :
    videofilepath = params.get("clip")
    jsonfilepath = params.get("json")
    outputpath = params.get("outputpath") if params.get("outputpath") else "./"

    sojufile= bu.get_sojufile_from_path(jsonfilepath)
    boomers = bu.get_boomers_from_dict(sojufile)
    generator = bu.prepare_boomer_generator(bu.get_boomer_generator_from_dict(sojufile))

    generator["generals"]["dropzone"] = outputpath

    print("wait a second...")
    await soju.audio_descriptor(videofilepath, generator)

    new_sojufile = bu.get_sojufile_from_path(outputpath + get_base_file_name_from(videofilepath) + ".soju.json")
    boomers = new_sojufile.get("generated") if new_sojufile.get("generated") else []
    boomers = boomers + [{
        "word": {
            "start": 888,
            "end": 888,
            "trigger": "start"
        },        
        "image": [
            {
                "duration": 0.3,
                "mergestrategy": "concat",
                "dir": "default",
                "file": "logo.png"
            }
        ],

        "audio": [
            {
                "duration": 0.3,
                "dir": "scary"
            }
        ]
        }]

    print("wait a moment...")
    await soju.video_editor(videofilepath, generator, boomers)










@listen()
async def on_startup():
    print("Bot is ready!")


@cooldown(Buckets.USER, 1, 7) 
@message_context_menu(
    name="Make it Silly",
)
async def prepare_and_edit(ctx: ContextMenuContext):

    try :
        clip_url = get_main_clip_url_from_referenced_message(ctx.target)
        clip_title = get_base_file_name_from(clip_url)

        if clip_title is None :
            raise Exception("No valid video attachments were found on the message you specified")

        await ctx.defer()
        with tempfile.TemporaryDirectory(dir="./") as tmp_dir_upload :
            output_clip_folder_path = tmp_dir_upload + "/"

            with tempfile.TemporaryDirectory(dir="./") as tmp_dir_download :
                input_clip_folder_path = tmp_dir_download + "/"

                download_file_from_url(clip_url, input_clip_folder_path + clip_title + ".mp4")

                mu.init_og_clip_params(input_clip_folder_path + clip_title + ".mp4")
                clip_h = mu.get_og_clip_params().get("height")
                clip_w = mu.get_og_clip_params().get("width")

                await edit({
                    "clip": input_clip_folder_path + clip_title + ".mp4",
                    "json": HORIZONTAL_GENERATOR_PATH if clip_h < clip_w else VERTICAL_GENERATOR_PATH,
                    "outputpath": output_clip_folder_path
                })

                await ctx.send(file= File(output_clip_folder_path + clip_title + ".mp4"))

    except Exception as err :
        await ctx.send(ephemeral= True, content= str(err))
    



bot.start()
