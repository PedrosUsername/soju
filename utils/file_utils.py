import random
import os
import itertools

from .settings import variables



HISTORY_LIMIT = 200



def get_base_file_name_from(videofilepath= None) :
    if videofilepath is None :
        return None
    
    filename = os.path.basename(videofilepath)
    _, tail = filename[::-1].split(".", 1)
    return tail[::-1]






def image_file_is_a_good_choice(path= "", image_file= "") :
    return os.path.isfile('{0}{1}'.format(path, image_file)) and image_file not in variables.IGNORE_IMAGE_FILE_LIST

def audio_file_is_a_good_choice(path= "", audio_file= "") :
    return os.path.isfile('{0}{1}'.format(path, audio_file)) and audio_file not in variables.IGNORE_AUDIO_FILE_LIST

def video_file_is_a_good_choice(path= "", video_file= "") :
    return os.path.isfile('{0}{1}'.format(path, video_file)) and video_file not in variables.IGNORE_VIDEO_FILE_LIST

def getFile(files= []) :
    if len(files) > 0:
        return random.choice(files)
    
    else:
        return None


























def getValidImageFiles(path= None) :
    image_files = os.listdir(path)

    if variables.DEFAULT_IMAGE_FILE != None:
        return [variables.DEFAULT_IMAGE_FILE]
    else:
        return [file for file in image_files if image_file_is_a_good_choice(path, file)]


def getValidAudioFiles(path= None) :
    audio_files = os.listdir(path)

    if variables.DEFAULT_AUDIO_FILE != None:
        return [variables.DEFAULT_AUDIO_FILE]        
    else:
        return [file for file in audio_files if audio_file_is_a_good_choice(path, file)]    


def getValidVideoFiles(path= None) :
    video_files = os.listdir(path)

    if variables.DEFAULT_VIDEO_FILE != None:
        return [variables.DEFAULT_VIDEO_FILE]
    else:
        return [file for file in video_files if video_file_is_a_good_choice(path, file)]



















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




async def get_random_media_inputs_from_channel(channel= None) :  
    if not channel:
        return ([], [], [])
    
    msgs = [message async for message in channel.history(limit=HISTORY_LIMIT)]

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
 
    return img, aud, vid





async def getValidMediaFilesFromDiscordByChannelId(channel_id= None, client= None) :
    return await get_random_media_inputs_from_channel(channel= client.get_channel(channel_id))