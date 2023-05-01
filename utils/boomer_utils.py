import json
import requests
import random

from .settings import variables
from . import Boomer as bmr



OVERLAY_SIZE_TOLERANCE = variables.OVERLAY_SIZE_TOLERANCE





def filterBoomers(og_clip_duration= 0, boomers= []):
    out_of_bounds_boomers_bot = []
    regular_boomers = []
    out_of_bounds_boomers_top = []

    for boomer in boomers:
        boomin_time = getBoomerBoominTime(boomer)
        if boomin_time > 0 and boomin_time < og_clip_duration:
            regular_boomers = regular_boomers + [boomer]
        elif boomin_time <= 0:
            out_of_bounds_boomers_bot = out_of_bounds_boomers_bot + [boomer]
        elif boomin_time >= og_clip_duration:
            out_of_bounds_boomers_top = out_of_bounds_boomers_top + [boomer]

    return (out_of_bounds_boomers_top, regular_boomers, out_of_bounds_boomers_bot)










def get_boomers(jsonfilepath):
    describe_json = []

    with open(jsonfilepath, 'r') as f:
        describe_json = f.read()

    return json.loads(describe_json)["soju"]["boomers"]






def get_boomers_from_url(jsonfilepath):
    response = requests.get(jsonfilepath)
    data = "{}"

    if (response.status_code):
        data = response.text
    
    return json.loads(data)["soju"]["boomers"]







def getBoomerImageWidth(boomer= None, main_clip_width= 0):
    if (
        not boomer
        or not boomer.get("image")
        or not boomer.get("image").get("conf")
        or not boomer.get("image").get("conf").get("width")
    ):
        return -1
    elif (main_clip_width + OVERLAY_SIZE_TOLERANCE) < boomer.get("image").get("conf").get("width"):
        return main_clip_width + OVERLAY_SIZE_TOLERANCE
    else:    
        return abs(boomer.get("image").get("conf").get("width"))
    







def getBoomerImageHeight(boomer= None, main_clip_height= 0):
    if (
        not boomer
        or not boomer.get("image")
        or not boomer.get("image").get("conf")
        or not boomer.get("image").get("conf").get("height")
    ):
        return main_clip_height + OVERLAY_SIZE_TOLERANCE
    elif (main_clip_height + OVERLAY_SIZE_TOLERANCE) < boomer.get("image").get("conf").get("height"):
        return main_clip_height + OVERLAY_SIZE_TOLERANCE
    else:    
        return abs(boomer.get("image").get("conf").get("height"))    
    







def getBoomerVideoWidth(boomer= None, main_clip_width= 0):
    if (
        not boomer
        or not boomer.get("video")
        or not boomer.get("video").get("conf")
        or not boomer.get("video").get("conf").get("width")
    ):
        return -1
    elif (main_clip_width + OVERLAY_SIZE_TOLERANCE) < boomer.get("video").get("conf").get("width"):
        return main_clip_width + OVERLAY_SIZE_TOLERANCE
    else:    
        return abs(boomer.get("video").get("conf").get("width"))
    





def getBoomerVideoHeight(boomer= None, main_clip_height= 0):
    if (
        not boomer
        or not boomer.get("video")
        or not boomer.get("video").get("conf")
        or not boomer.get("video").get("conf").get("height")
    ):
        return main_clip_height + OVERLAY_SIZE_TOLERANCE
    elif (main_clip_height + OVERLAY_SIZE_TOLERANCE) < boomer.get("video").get("conf").get("height"):
        return main_clip_height + OVERLAY_SIZE_TOLERANCE
    else:    
        return abs(boomer.get("video").get("conf").get("height"))    







def getBoomTrigger(boomer= None):
    if (
        not boomer
        or not boomer.get("word")
        or not boomer.get("word").get("trigger")
    ):
        return variables.DEFAULT_BOOM_TRIGGER if variables.DEFAULT_BOOM_TRIGGER else "end"
    else:
        return boomer.get("word").get("trigger")







def getBoomerBoominTime(boomer= None):
    trigg = getBoomTrigger(boomer)
    if (
        not boomer
        or not boomer.get("word")
        or not boomer.get("word").get(trigg)
    ):
        return 0
    else:
        return float(boomer.get("word").get(trigg))









def getBoomerImageDuration(boomer= None):
    if (
        not boomer
        or not boomer.get("image") 
        or not boomer.get("image").get("conf")
        or not boomer.get("image").get("conf").get("duration")
    ):
        return 0
    else:
        return boomer.get("image").get("conf").get("duration")








def getBoomerAudioDuration(boomer= None):
    if (
        not boomer
        or not boomer.get("audio") 
        or not boomer.get("audio").get("conf")
        or not boomer.get("audio").get("conf").get("duration")
    ):
        return 0
    else:
        return boomer.get("audio").get("conf").get("duration")
    






def getBoomerVideoDuration(boomer= None):
    if (
        not boomer
        or not boomer.get("video") 
        or not boomer.get("video").get("conf")
        or not boomer.get("video").get("conf").get("duration")
    ):
        return 0
    else:
        return boomer.get("video").get("conf").get("duration")











def getBoomerVideoVolume(boomer= None):
    if (
        not boomer
        or not boomer.get("video")
        or not boomer.get("video").get("conf")
        or not boomer.get("video").get("conf").get("volume")
    ):
        if boomer.get("video").get("conf").get("volume") == 0:
            return 0
        else:
            return 1
    else:
        return boomer.get("video").get("conf").get("volume")
    







def getBoomerAudioVolume(boomer= None):
    if (
        not boomer
        or not boomer.get("video")
        or not boomer.get("video").get("conf")
        or not boomer.get("audio").get("conf").get("volume")
    ):
        if boomer.get("audio").get("conf").get("volume") == 0:
            return 0
        else:
            return 1
    else:
        return boomer.get("audio").get("conf").get("volume")    









def getFile(files= []):
    if len(files) > 0:
        return random.choice(files)
    
    else:
        return None



def buildBoomer(obj, image_files, audio_files, video_files):
    image_file = getFile(image_files)
    audio_file = getFile(audio_files)
    video_file = getFile(video_files)

    obj["word"] = {
        "content": obj["word"],
        "start": obj["start"],
        "end": obj["end"],
        "trigger": variables.DEFAULT_BOOM_TRIGGER
    }

    obj["image"] = {
        "file": image_file,
        "conf": {
            "height": variables.DEFAULT_IMAGE_RESOLUTION_HEIGHT,
            "width": variables.DEFAULT_IMAGE_RESOLUTION_WIDTH,
            "mergestrategy": variables.DEFAULT_IMAGE_CONCAT_STRATEGY,
            "duration": variables.MAX_IMAGE_DURATION,
        }
    }    

    obj["audio"] = {
        "file": audio_file,
        "conf": {
            "duration": variables.MAX_AUDIO_DURATION,
            "volume": variables.DEFAULT_AUDIO_VOLUME
        }
    }

    obj["video"] = {
        "file": video_file,
        "conf": {
            "height": variables.DEFAULT_VIDEO_RESOLUTION_HEIGHT,
            "width": variables.DEFAULT_VIDEO_RESOLUTION_WIDTH,
            "mergestrategy": variables.DEFAULT_VIDEO_MERGE_STRATEGY,
            "duration": variables.MAX_VIDEO_DURATION,
            "volume": variables.DEFAULT_VIDEO_VOLUME,
        }
    }

    return bmr.Boomer(obj)













def buildSilentBoomer(obj, image_files, video_files):
    image_file = getFile(image_files)
    video_file = getFile(video_files)

    obj["word"] = {
        "content": obj["word"],
        "start": obj["start"],
        "end": obj["end"],
        "trigger": variables.DEFAULT_BOOM_TRIGGER
    }

    rand = random.choice(range(2))

    if rand :
        obj["image"] = {
            "file": image_file,
            "conf": {
                "height": variables.DEFAULT_IMAGE_RESOLUTION_HEIGHT,
                "width": variables.DEFAULT_IMAGE_RESOLUTION_WIDTH,
                "mergestrategy": variables.DEFAULT_IMAGE_CONCAT_STRATEGY,
                "duration": variables.MAX_IMAGE_DURATION,
            }
        }
        
        obj["video"] = None
    
    else :
        obj["video"] = {
            "file": video_file,
            "conf": {
                "height": variables.DEFAULT_VIDEO_RESOLUTION_HEIGHT,
                "width": variables.DEFAULT_VIDEO_RESOLUTION_WIDTH,
                "mergestrategy": variables.DEFAULT_VIDEO_MERGE_STRATEGY,
                "duration": variables.MAX_VIDEO_DURATION,
                "volume": variables.DEFAULT_VIDEO_VOLUME,
            }
        }

        obj["image"] = None

    obj["audio"] = None

    return bmr.Boomer(obj)
