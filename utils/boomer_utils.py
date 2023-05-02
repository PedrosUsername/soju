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








def get_boomers_from_dict(sojufile= None) :
    if (
        not sojufile
        or not sojufile.get("soju")
        or not sojufile.get("soju").get("boomers")
    ) :
        return []
    
    else :
        return sojufile.get("soju").get("boomers")






def get_boomers_from_file(jsonfilepath) :
    describe_json = []

    with open(jsonfilepath, 'r') as f:
        describe_json = f.read()

    return json.loads(describe_json)["soju"]["boomers"]








def get_boomer_generator_from_dict(sojufile= None) :
    if (
        not sojufile
        or not sojufile.get("soju")
        or not sojufile.get("soju").get("generator")
    ) :
        return []
    
    else :
        return sojufile.get("soju").get("generator")







def get_boomer_generator_from_file(jsonfilepath) :
    describe_json = []

    with open(jsonfilepath, 'r') as f:
        describe_json = f.read()

    return json.loads(describe_json)["soju"]["generator"]









def get_boomers_from_url(jsonfilepath):
    
    data = get_sojufile_confs_from_url(jsonfilepath)
    return data.get("boomers") if data is not None else None








def get_boomer_generator_from_url(jsonfilepath):
    
    data = get_sojufile_confs_from_url(jsonfilepath)
    return data.get("generator") if data is not None else None







def get_sojufile_confs_from_url(jsonfilepath):
    if not str(jsonfilepath).endswith(".json") :
        return None
    

    response = requests.get(jsonfilepath)
    data = "{}"

    if (response.status_code):
        data = response.text
    
    return json.loads(data).get("soju")







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
    ):
        return None
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
        boomer is None
        or boomer.get("video") is None
        or boomer.get("video").get("conf") is None
    ):
        return None

    else:
        return boomer.get("video").get("conf").get("volume")
    







def getBoomerAudioVolume(boomer= None):
    if (
        boomer is None
        or boomer.get("audio") is None
        or boomer.get("audio").get("conf") is None
    ):
        return None

    else:
        return boomer.get("audio").get("conf").get("volume")    









def getBoomerImageFile(boomer= None) :
    if (
        not boomer
        or not boomer.get("image") 
    ):
        return None
    else:
        return boomer.get("image").get("file")






def getBoomerAudioFile(boomer= None) :
    if (
        not boomer
        or not boomer.get("audio") 
    ):
        return None
    else:
        return boomer.get("audio").get("file")










def getBoomerVideoFile(boomer= None) :
    if (
        not boomer
        or not boomer.get("video") 
    ):
        return None
    else:
        return boomer.get("video").get("file")








def getBoomerImageMergeStrategy(boomer= None) :
    if (
        not boomer
        or not boomer.get("image")
        or not boomer.get("image").get("conf")
    ):
        return None
    else:
        return boomer.get("image").get("conf").get("mergestratagy")








def getBoomerVideoMergeStrategy(boomer= None) :
    if (
        not boomer
        or not boomer.get("video")
        or not boomer.get("video").get("conf")
    ):
        return None
    else:
        return boomer.get("video").get("conf").get("mergestratagy")











def getBoomerImagePosX(boomer= None) :
    if (
        not boomer
        or not boomer.get("image")
        or not boomer.get("image").get("conf")
    ):
        return None
    else:
        return boomer.get("image").get("conf").get("posx")



def getBoomerImagePosY(boomer= None) :
    if (
        not boomer
        or not boomer.get("image")
        or not boomer.get("image").get("conf")
    ):
        return None
    else:
        return boomer.get("image").get("conf").get("posy")




def getBoomerVideoPosX(boomer= None) :
    if (
        not boomer
        or not boomer.get("video")
        or not boomer.get("video").get("conf")
    ):
        return None
    else:
        return boomer.get("video").get("conf").get("posx")



def getBoomerVideoPosY(boomer= None) :
    if (
        not boomer
        or not boomer.get("video")
        or not boomer.get("video").get("conf")
    ):
        return None
    else:
        return boomer.get("video").get("conf").get("posy")





def getBoomerImageTriggerDelay(boomer= None) :
    if (
        not boomer
        or not boomer.get("image")
        or not boomer.get("image").get("conf")
    ):
        return None
    else:
        return boomer.get("image").get("conf").get("triggerdelay")




def getBoomerVideoTriggerDelay(boomer= None) :
    if (
        not boomer
        or not boomer.get("video")
        or not boomer.get("video").get("conf")
    ):
        return None
    else:
        return boomer.get("video").get("conf").get("triggerdelay")








def getBoomerAudioTriggerDelay(boomer= None) :
    if (
        not boomer
        or not boomer.get("audio")
        or not boomer.get("audio").get("conf")
    ):
        return None
    else:
        return boomer.get("audio").get("conf").get("triggerdelay")











def getDefaultResoTol(default= None) :
    if (
        not default
        or not default.get("general")
    ):
        return None
    else:
        return default.get("general").get("resotolerance")
    











def getDefaultApiName(default= None) :
    if (
        not default
        or not default.get("general")
        or not default.get("general").get("api")
    ):
        return None
    else:
        return default.get("general").get("api").get("name")












def getDefaultApiModel(default= None) :
    if (
        not default
        or not default.get("general")
        or not default.get("general").get("api")
    ):
        return None
    else:
        return default.get("general").get("api").get("model")    



























































def get_boomer_generator_as_str(generator= None) :

    if generator is not None :
        default = generator.get("defaults")

        dresotol = getDefaultResoTol(default)
        dapin = getDefaultApiName(default)
        dapim = getDefaultApiModel(default)

        dbt = getBoomTrigger(default)

        dimgf = getBoomerImageFile(default)
        dimgms = getBoomerImageMergeStrategy(default)
        dimgdur = getBoomerImageDuration(default)
        dimgh = getBoomerImageHeight(default)
        dimgw = getBoomerImageWidth(default)
        dimgx = getBoomerImagePosX(default)
        dimgy = getBoomerImagePosY(default)
        dimgd = getBoomerImageTriggerDelay(default)

        dvidf = getBoomerVideoFile(default)
        dvidms = getBoomerVideoMergeStrategy(default)
        dviddur = getBoomerVideoDuration(default)
        dvidh = getBoomerVideoHeight(default)
        dvidw = getBoomerVideoWidth(default)
        dvidx = getBoomerVideoPosX(default)
        dvidy = getBoomerVideoPosY(default)
        dvidd = getBoomerVideoTriggerDelay(default)
        dvidvol = getBoomerVideoVolume(default)

        daudf = getBoomerAudioFile(default)
        dauddur = getBoomerAudioDuration(default)
        daudd = getBoomerAudioTriggerDelay(default)
        daudvol = getBoomerAudioVolume(default)

    else :
        dresotol = variables.OVERLAY_SIZE_TOLERANCE
        dapin = variables.DEFAULT_API_NAME
        dapim = variables.DEFAULT_API_MODEL

        dbt = variables.DEFAULT_BOOM_TRIGGER

        dimgf = variables.DEFAULT_IMAGE_FILE
        dimgms = variables.DEFAULT_IMAGE_MERGE_STRATEGY
        dimgdur = variables.DEFAULT_IMAGE_DURATION
        dimgh = variables.DEFAULT_IMAGE_RESOLUTION_HEIGHT
        dimgw = variables.DEFAULT_IMAGE_RESOLUTION_WIDTH
        dimgx = variables.DEFAULT_IMAGE_POSITION_X
        dimgy = variables.DEFAULT_IMAGE_POSITION_Y
        dimgd = variables.DEFAULT_IMAGE_TRIGGER_DELAY

        dvidf = variables.DEFAULT_VIDEO_FILE
        dvidms = variables.DEFAULT_VIDEO_MERGE_STRATEGY
        dviddur = variables.DEFAULT_VIDEO_DURATION
        dvidh = variables.DEFAULT_VIDEO_RESOLUTION_HEIGHT
        dvidw = variables.DEFAULT_VIDEO_RESOLUTION_WIDTH
        dvidx = variables.DEFAULT_VIDEO_POSITION_X
        dvidy = variables.DEFAULT_VIDEO_POSITION_Y
        dvidd = variables.DEFAULT_VIDEO_TRIGGER_DELAY
        dvidvol = variables.DEFAULT_VIDEO_VOLUME

        daudf = variables.DEFAULT_AUDIO_FILE
        dauddur = variables.DEFAULT_AUDIO_DURATION
        daudd = variables.DEFAULT_AUDIO_TRIGGER_DELAY
        daudvol = variables.DEFAULT_AUDIO_VOLUME        


    dresotol = "null" if dresotol is None else dresotol
    dapin = "null" if dapin is None else dapin
    dapim = "null" if dapim is None else dapim

    dbt = "null" if dbt is None else dbt

    dimgf = "null" if dimgf is None else dimgf
    dimgms = "null" if dimgms is None else dimgms
    dimgdur = "null" if dimgdur is None else dimgdur               # never null!
    dimgh = "null" if dimgh is None else dimgh                     # never null!
    dimgw = "null" if dimgw is None else dimgw                     # never null!
    dimgx = "null" if dimgx is None else dimgx
    dimgy = "null" if dimgy is None else dimgy
    dimgd = "null" if dimgd is None else dimgd

    dvidf = "null" if dvidf is None else dvidf
    dvidms = "null" if dvidms is None else dvidms
    dviddur = "null" if dviddur is None else dviddur               # never null!
    dvidh = "null" if dvidh is None else dvidh                     # never null!
    dvidw = "null" if dvidw is None else dvidw                     # never null!
    dvidx = "null" if dvidx is None else dvidx
    dvidy = "null" if dvidy is None else dvidy
    dvidd = "null" if dvidd is None else dvidd
    dvidvol = "null" if dvidvol is None else dvidvol               

    daudf = "null" if daudf is None else daudf
    dauddur = "null" if dauddur is None else dauddur               # never null!
    daudd = "null" if daudd is None else daudd
    daudvol = "null" if daudvol is None else daudvol


    
    return f""" {{
                    "general": {{
                        "resotolerance": {dresotol},
                        
                        "api": {{
                            "name": {dapin},
                            "model": {dapim}
                        }}
                    }},

                    "defaults": {{
                        "word": {{
                            "trigger": {dbt}
                        }},

                        "image": {{
                            "file": {dimgf},
                            "conf": {{
                                "mergestrategy": {dimgms},
                                "duration": {dimgdur},
                                "height": {dimgh},
                                "width": {dimgw},               
                                "posx": {dimgx},
                                "posy": {dimgy},
                                "triggerdelay": {dimgd}
                            }}

                        }},

                        "video": {{
                            "file": {dvidf},
                            "conf": {{
                                "mergestrategy": {dvidms},
                                "duration": {dviddur},
                                "height": {dvidh},
                                "width": {dvidw},               
                                "posx": {dvidx},
                                "posy": {dvidy},
                                "triggerdelay": {dvidd},
                                "volume": {dvidvol}
                            }}
                        }},

                        "audio": {{
                            "file": {daudf},
                            "conf": {{
                                "duration": {dauddur},
                                "triggerdelay": {daudd},
                                "volume": {daudvol}
                            }}
                        }}
                    }}
                }}"""






def get_boomer_generator_as_dict(generator= None) :
    return json.loads(get_boomer_generator_as_str(generator))












def getFile(files= []):
    if len(files) > 0:
        return random.choice(files)
    
    else:
        return None



def buildBoomer(obj, image_files= [], audio_files= [], video_files= [], generator= None):

    b_gen = get_boomer_generator_as_dict(generator)
    default = b_gen.get("defaults")

    obj["word"] = {
        "content": obj["word"],
        "start": obj["start"],
        "end": obj["end"],
        "trigger": getBoomTrigger(default)
    }

    obj["image"] = {
        "file": getBoomerImageFile(default),
        "conf": {
            "mergestrategy": getBoomerImageMergeStrategy(default),
            "duration": getBoomerImageDuration(default),
            "height": getBoomerImageHeight(default),
            "width": getBoomerImageWidth(default),
            "posx": getBoomerImagePosX(default),
            "posy": getBoomerImagePosY(default),
            "triggerdelay": getBoomerImageWidth(default),
        }
    }    

    obj["audio"] = {
        "file": getBoomerAudioFile(default),
        "conf": {
            "duration": getBoomerAudioDuration(default),
            "triggerdelay": getBoomerImageWidth(default),
            "volume": getBoomerAudioVolume(default)
        }
    }

    obj["video"] = {
        "file": getBoomerVideoFile(default),
        "conf": {
            "mergestrategy": getBoomerVideoMergeStrategy(default),
            "duration": getBoomerVideoDuration(default),
            "height": getBoomerVideoHeight(default),
            "width": getBoomerVideoWidth(default),
            "posx": getBoomerVideoPosX(default),
            "posy": getBoomerVideoPosY(default),
            "triggerdelay": getBoomerVideoWidth(default),
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
