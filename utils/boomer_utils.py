import json
import requests
import random

from .settings import variables
from .enum.Enum import MergeStrategy, Trigger
from . import Boomer as bmr



OVERLAY_SIZE_TOLERANCE = variables.OVERLAY_SIZE_TOLERANCE
OVERLAY_SIZE_TOLERANCE = variables.OVERLAY_SIZE_TOLERANCE
MAX_MEDIA_INSERT_DURATION = variables.MAX_MEDIA_INSERT_DURATION
MIN_MEDIA_INSERT_DURATION = variables.MIN_MEDIA_INSERT_DURATION
MAX_MEDIA_VOLUME = variables.MAX_MEDIA_VOLUME
MIN_MEDIA_VOLUME = variables.MIN_MEDIA_VOLUME




def classifyBoomersByImageMergeStrategy(boomers= []):
    image_files_compose = []
    image_files_concat = []

    for b in boomers:
        strategy = getBoomerImageMergeStrategyForFFMPEG(b)

        if strategy == MergeStrategy.get("COMPOSE") :

            image_files_compose = image_files_compose + [b]
        elif strategy == MergeStrategy.get("CONCAT") :

            image_files_concat = image_files_concat + [b]

    return (image_files_compose, image_files_concat)






def classifyBoomersByVideoMergeStrategy(boomers= []):
    video_files_compose = []
    video_files_concat = []

    for b in boomers:
        strategy = getBoomerVideoMergeStrategyForFFMPEG(b)

        if strategy == MergeStrategy.get("COMPOSE") :

            video_files_compose = video_files_compose + [b]
        elif strategy == MergeStrategy.get("CONCAT") :

            video_files_concat = video_files_concat + [b]

    return (video_files_compose, video_files_concat)







def filterBoomers(og_clip_duration= 0, boomers= []):
    out_of_bounds_boomers_bot = []
    regular_boomers = []
    out_of_bounds_boomers_top = []

    for boomer in boomers:
        boomin_time = getBoomerBoominTimeForFFMPEG(boomer)
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
    ) :
        return None
    
    else :
        return sojufile.get("boomers")






def get_boomers_from_file(jsonfilepath) :
    describe_json = []

    with open(jsonfilepath, 'r') as f:
        describe_json = f.read()

    return json.loads(describe_json)["soju"]["boomers"]








def get_boomer_generator_from_dict(sojufile= None) :
    if not sojufile :
        return None
    
    else :
        return sojufile.get("generator")







def get_boomer_generator_from_file(jsonfilepath) :
    describe_json = []

    with open(jsonfilepath, 'r') as f:
        describe_json = f.read()

    generator = json.loads(describe_json)
    if (
        not generator
        or not generator.get("soju")
        or not generator.get("soju").get("generator")
    ) :
        return None
    else :
        return generator.get("soju").get("generator")









def get_boomers_from_url(jsonfilepath):
    
    data = get_sojufile_from_url_as_dict(jsonfilepath)
    return data.get("boomers") if data is not None else None








def get_boomer_generator_from_url(jsonfilepath):
    
    data = get_sojufile_from_url_as_dict(jsonfilepath)
    return data.get("generator") if data is not None else None







def get_sojufile_from_url_as_dict(jsonfilepath):
    if not str(jsonfilepath).endswith(".json") :
        return None
    

    response = requests.get(jsonfilepath)
    data = "{}"

    if (response.status_code):
        data = response.text
    
    return json.loads(data).get("soju")


















def getBoomerImageFileForFFMPEG(boomer= None) :
    file = getBoomerImageFile(boomer)

    if file is None :
        return 
    else :
        return file

def getBoomerImagePosXForFFMPEG(boomer= None) :
    x = getBoomerImagePosX(boomer)

    if x is None :
        return 0
    
    else :
        return x
    

def getBoomerImagePosYForFFMPEG(boomer= None) :
    y = getBoomerImagePosY(boomer)

    if y is None :
        return 0
   
    else :
        return y    
    


def getBoomerVideoPosXForFFMPEG(boomer= None) :
    x = getBoomerVideoPosX(boomer)

    if x is None :
        return 0
    
    else :
        return x
    

def getBoomerVideoPosYForFFMPEG(boomer= None) :
    y = getBoomerVideoPosY(boomer)

    if y is None :
        return 0
   
    else :
        return y    





def getBoomerImageMergeStrategyForFFMPEG(boomer= None) :
    ms = getBoomerImageMergeStrategy(boomer)

    if ms is None :
        return MergeStrategy.get("COMPOSE")
   
    else :
        return ms
    


def getBoomerVideoMergeStrategyForFFMPEG(boomer= None) :
    ms = getBoomerVideoMergeStrategy(boomer)

    if ms is None :
        return MergeStrategy.get("COMPOSE")
   
    else :
        return ms    



def getBoomerImageWidthForFFMPEG(boomer, main_clip_width= 0) :
    w = getBoomerImageWidth(boomer)

    if w is None:
        return -1
    
    elif (main_clip_width + OVERLAY_SIZE_TOLERANCE) < w :
        return main_clip_width + OVERLAY_SIZE_TOLERANCE
    
    else:    
        return abs(w)
    


def getBoomerVideoWidthForFFMPEG(boomer, main_clip_width= 0) :
    w = getBoomerVideoWidth(boomer)

    if w is None:

        return -1
    elif (main_clip_width + OVERLAY_SIZE_TOLERANCE) < w :
        
        return main_clip_width + OVERLAY_SIZE_TOLERANCE
    else:    
        return abs(w)    






def getBoomerImageHeightForFFMPEG(boomer= None, main_clip_height= 0):
    h = getBoomerImageHeight(boomer)

    if h is None:

        return main_clip_height + OVERLAY_SIZE_TOLERANCE
    elif (main_clip_height + OVERLAY_SIZE_TOLERANCE) < h:

        return main_clip_height + OVERLAY_SIZE_TOLERANCE
    else:    
        return abs(h)    
    



def getBoomerVideoHeightForFFMPEG(boomer= None, main_clip_height= 0):
    h = getBoomerVideoHeight(boomer)

    if h is None:

        return main_clip_height + OVERLAY_SIZE_TOLERANCE
    elif (main_clip_height + OVERLAY_SIZE_TOLERANCE) < h:

        return main_clip_height + OVERLAY_SIZE_TOLERANCE
    else:    
        return abs(h)    



def getBoomerImageDurationForFFMPEG(boomer= None) :
    dur = getBoomerImageDuration(boomer)

    if dur is None :
        return 0
    else :
        if dur > MAX_MEDIA_INSERT_DURATION :
            return MAX_MEDIA_INSERT_DURATION
        
        elif dur < MIN_MEDIA_INSERT_DURATION :
            return MIN_MEDIA_INSERT_DURATION
        
        else :
            return dur



def getBoomerAudioDurationForFFMPEG(boomer= None) :
    dur = getBoomerAudioDuration(boomer)

    if dur is None :
        return 0
    else :
        if dur > MAX_MEDIA_INSERT_DURATION :
            return MAX_MEDIA_INSERT_DURATION
        
        elif dur < MIN_MEDIA_INSERT_DURATION :
            return MIN_MEDIA_INSERT_DURATION
        
        else :
            return dur



def getBoomerVideoDurationForFFMPEG(boomer= None) :
    dur = getBoomerVideoDuration(boomer)

    if dur is None :
        return 0
    
    else :
        if dur > MAX_MEDIA_INSERT_DURATION :
            return MAX_MEDIA_INSERT_DURATION
        
        elif dur < MIN_MEDIA_INSERT_DURATION :
            return MIN_MEDIA_INSERT_DURATION
        
        else :
            return dur        



def getBoomerBoominTimeForFFMPEG(boomer= None) :
    time = getBoomerBoominTime(boomer)

    if time is None :
        return 0
    else :
        return time



def getBoomerVideoVolumeForFFMPEG(boomer= None) :
    vol = getBoomerVideoVolume(boomer)

    if vol is None :
        return 0.1
    else :
        if vol > MAX_MEDIA_VOLUME :
            return MAX_MEDIA_VOLUME
        
        elif vol < MIN_MEDIA_VOLUME :
            return MIN_MEDIA_VOLUME
        
        else :
            return vol
        

def getBoomerAudioVolumeForFFMPEG(boomer= None) :
    vol = getBoomerAudioVolume(boomer)

    if vol is None :
        return 1
    else :
        if vol > MAX_MEDIA_VOLUME :
            return MAX_MEDIA_VOLUME
        
        elif vol < MIN_MEDIA_VOLUME :
            return MIN_MEDIA_VOLUME
        
        else :
            return vol











def getBoomerImageWidth(boomer= None):
    if (
        not boomer
        or not boomer.get("image")
        or not boomer.get("image").get("conf")
    ):
        return None
    else:    
        return boomer.get("image").get("conf").get("width")
    







def getBoomerImageHeight(boomer= None):
    if (
        not boomer
        or not boomer.get("image")
        or not boomer.get("image").get("conf")
    ):
        return None
    else:    
        return boomer.get("image").get("conf").get("height")    
    







def getBoomerVideoWidth(boomer= None):
    if (
        not boomer
        or not boomer.get("video")
        or not boomer.get("video").get("conf")
    ):
        return None
    else:    
        return boomer.get("video").get("conf").get("width")
    





def getBoomerVideoHeight(boomer= None):
    if (
        not boomer
        or not boomer.get("video")
        or not boomer.get("video").get("conf")
    ):
        return None
    else:    
        return boomer.get("video").get("conf").get("height")    







def getBoomTrigger(boomer= None):
    if (
        not boomer
        or not boomer.get("word")
    ):
        return None
    else:
        return boomer.get("word").get("trigger")






def getBoomTriggerForFFMPEG(boomer= None) :
    trigg = getBoomTrigger(boomer)

    if trigg is None :
        return Trigger.get("START")
    else :
        return trigg


def getBoomerBoominTime(boomer= None):
    trigg = getBoomTrigger(boomer)

    if (
        not boomer
        or not trigg
        or not boomer.get("word")
        or not boomer.get("word").get(trigg)
    ):
        return None
    else:
        return float(boomer.get("word").get(trigg))









def getBoomerImageDuration(boomer= None):
    if (
        not boomer
        or not boomer.get("image") 
        or not boomer.get("image").get("conf")
    ):
        return None
    else:
        return boomer.get("image").get("conf").get("duration")








def getBoomerAudioDuration(boomer= None):
    if (
        not boomer
        or not boomer.get("audio") 
        or not boomer.get("audio").get("conf")
    ):
        return None
    else:
        return boomer.get("audio").get("conf").get("duration")
    






def getBoomerVideoDuration(boomer= None):
    if (
        not boomer
        or not boomer.get("video") 
        or not boomer.get("video").get("conf")
    ):
        return None
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
        return boomer.get("image").get("conf").get("mergestrategy")








def getBoomerVideoMergeStrategy(boomer= None) :
    if (
        not boomer
        or not boomer.get("video")
        or not boomer.get("video").get("conf")
    ):
        return None
    else:
        return boomer.get("video").get("conf").get("mergestrategy")











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
























































def as_json_string(value) :
    try :
        return '"' + str(value) + '"'
    except ValueError :
        return "null"

def as_json_integer(value) :
    try :
        return int(value)
    except ValueError :
        return 0

def as_json_float(value) :
    try :
        return float(value)
    except ValueError :
        return 0



def get_boomer_generator_as_str(generator= None) :

    if (
        generator is not None
        and generator.get("defaults") is not None
    ) :
        default = generator.get("defaults")

        dresotol = getDefaultResoTol(default)
        dapin = getDefaultApiName(default)
        dapim = getDefaultApiModel(default)

        dbt = getBoomTriggerForFFMPEG(default)

        dimgf = getBoomerImageFile(default)
        dimgms = getBoomerImageMergeStrategyForFFMPEG(default)
        dimgdur = getBoomerImageDurationForFFMPEG(default)
        dimgh = getBoomerImageHeightForFFMPEG(default)
        dimgw = getBoomerImageWidthForFFMPEG(default)
        dimgx = getBoomerImagePosXForFFMPEG(default)
        dimgy = getBoomerImagePosYForFFMPEG(default)
        dimgd = getBoomerImageTriggerDelay(default)

        dvidf = getBoomerVideoFile(default)
        dvidms = getBoomerVideoMergeStrategyForFFMPEG(default)
        dviddur = getBoomerVideoDurationForFFMPEG(default)
        dvidh = getBoomerVideoHeightForFFMPEG(default)
        dvidw = getBoomerVideoWidthForFFMPEG(default)
        dvidx = getBoomerVideoPosXForFFMPEG(default)
        dvidy = getBoomerVideoPosYForFFMPEG(default)
        dvidd = getBoomerVideoTriggerDelay(default)
        dvidvol = getBoomerVideoVolumeForFFMPEG(default)

        daudf = getBoomerAudioFile(default)
        dauddur = getBoomerAudioDurationForFFMPEG(default)
        daudd = getBoomerAudioTriggerDelay(default)
        daudvol = getBoomerAudioVolumeForFFMPEG(default)

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


    dresotol = "null" if dresotol is None else as_json_integer(dresotol)
    dapin = "null" if dapin is None else as_json_string(dapin)
    dapim = "null" if dapim is None else as_json_string(dapim)

    dbt = "null" if dbt is None else as_json_string(dbt)

    dimgf = "null" if dimgf is None else as_json_string(dimgf)
    dimgms = "null" if dimgms is None else as_json_string(dimgms)
    dimgdur = "null" if dimgdur is None else as_json_float(dimgdur)               
    dimgh = "null" if dimgh is None else as_json_integer(dimgh)                     
    dimgw = "null" if dimgw is None else as_json_integer(dimgw)                     
    dimgx = "null" if dimgx is None else as_json_string(dimgx)
    dimgy = "null" if dimgy is None else as_json_string(dimgy)
    dimgd = "null" if dimgd is None else as_json_float(dimgd)

    dvidf = "null" if dvidf is None else as_json_string(dvidf)
    dvidms = "null" if dvidms is None else as_json_string(dvidms)
    dviddur = "null" if dviddur is None else as_json_float(dviddur)               
    dvidh = "null" if dvidh is None else as_json_integer(dvidh)                     
    dvidw = "null" if dvidw is None else as_json_integer(dvidw)                     
    dvidx = "null" if dvidx is None else as_json_string(dvidx)
    dvidy = "null" if dvidy is None else as_json_string(dvidy)
    dvidd = "null" if dvidd is None else as_json_float(dvidd)
    dvidvol = "null" if dvidvol is None else as_json_float(dvidvol)               

    daudf = "null" if daudf is None else as_json_string(daudf)
    dauddur = "null" if dauddur is None else as_json_float(dauddur)               
    daudd = "null" if daudd is None else as_json_float(daudd)
    daudvol = "null" if daudvol is None else as_json_float(daudvol)
    
    return f""" {{
                    "general": {{
                        "resotolerance": {dresotol},
                        
                        "defaultimageset": "default",
                        "defaultvideoset": "default",
                        "defaultaudioset": "default",
                        "defaultsetshare": 0.5,

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
    aux = get_boomer_generator_as_str(generator)
    print(aux)
    return json.loads(aux)












def getFile(files= []):
    if len(files) > 0:
        return random.choice(files)
    
    else:
        return None



def buildBoomer(obj, image_files= [], audio_files= [], video_files= [], default= None):

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
            "triggerdelay": getBoomerImageTriggerDelay(default),
        }
    }    

    obj["audio"] = {
        "file": getBoomerAudioFile(default),
        "conf": {
            "duration": getBoomerAudioDuration(default),
            "triggerdelay": getBoomerAudioTriggerDelay(default),
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
            "triggerdelay": getBoomerVideoTriggerDelay(default),
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
