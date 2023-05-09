import json
import requests
import random

from .settings import variables
from .enum.Enum import MergeStrategy, Trigger, Position, ImageFilesDir, VideoFilesDir, AudioFilesDir
from . import Boomer as bmr, moviepy_utils as mp




DEFAULT_IMAGE_DIR = "DEFAULT"
DEFAULT_AUDIO_DIR = "DEFAULT"
DEFAULT_VIDEO_DIR = "DEFAULT"
MIN_RESOLUTION_SIZE = variables.MIN_RESOLUTION_SIZE
MAX_MEDIA_DELAY = variables.MAX_MEDIA_DELAY
MIN_MEDIA_DELAY = variables.MIN_MEDIA_DELAY
DEFAULT_VIDEO_FILE = variables.DEFAULT_VIDEO_FILE
DEFAULT_AUDIO_FILE = variables.DEFAULT_AUDIO_FILE
DEFAULT_IMAGE_FILE = variables.DEFAULT_IMAGE_FILE
DEFAULT_DELAY = variables.DEFAULT_IMAGE_TRIGGER_DELAY
DEFAULT_POSITION = Position.get("CENTER")
DEFAULT_VIDEO_WIDTH = variables.DEFAULT_VIDEO_RESOLUTION_WIDTH
DEFAULT_IMAGE_WIDTH = variables.DEFAULT_IMAGE_RESOLUTION_WIDTH
DEFAULT_IMAGE_MERGESTRATEGY = MergeStrategy.get("COMPOSE")
DEFAULT_VIDEO_MERGESTRATEGY = MergeStrategy.get("CONCAT")
DEFAULT_BOOM_TRIGGER = Trigger.get("START")
DEFAULT_API_NAME = variables.DEFAULT_API_NAME
DEFAULT_API_MODEL = variables.DEFAULT_API_MODEL
OVERLAY_SIZE_TOLERANCE = variables.OVERLAY_SIZE_TOLERANCE
MAX_MEDIA_INSERT_DURATION = variables.MAX_MEDIA_INSERT_DURATION
MIN_MEDIA_INSERT_DURATION = variables.MIN_MEDIA_INSERT_DURATION
MAX_MEDIA_VOLUME = variables.MAX_MEDIA_VOLUME
MIN_MEDIA_VOLUME = variables.MIN_MEDIA_VOLUME
DEFAULT_VIDEO_VOL = variables.DEFAULT_VIDEO_VOLUME
DEFAULT_AUDIO_VOL = variables.DEFAULT_AUDIO_VOLUME































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





























def getBoomerAudioTriggerDelayForFFMPEG(boomer= None) :
    td = getBoomerAudioTriggerDelay(boomer)

    if not isinstance(td, int) and not isinstance(td, float) :
        return DEFAULT_DELAY
    
    else :
        if td > MAX_MEDIA_DELAY :
            return MAX_MEDIA_DELAY
        
        elif td < MIN_MEDIA_DELAY :
            return MIN_MEDIA_DELAY
        
        else :
            return abs(td)




def getBoomerVideoTriggerDelayForFFMPEG(boomer= None) :
    td = getBoomerVideoTriggerDelay(boomer)

    if not isinstance(td, int) and not isinstance(td, float) :
        return DEFAULT_DELAY
    
    else :
        if td > MAX_MEDIA_DELAY :
            return MAX_MEDIA_DELAY
        
        elif td < MIN_MEDIA_DELAY :
            return MIN_MEDIA_DELAY
        
        else :
            return abs(td)






def getBoomerImageTriggerDelayForFFMPEG(boomer= None) :
    td = getBoomerImageTriggerDelay(boomer)

    if not isinstance(td, int) and not isinstance(td, float) :
        return DEFAULT_DELAY
    
    else :
        if td > MAX_MEDIA_DELAY :
            return MAX_MEDIA_DELAY
        
        elif td < MIN_MEDIA_DELAY :
            return MIN_MEDIA_DELAY
        
        else :
            return abs(td)




def getBoomerImageFileForFFMPEG(boomer= None, files= []) :
    file = getBoomerImageFile(boomer)

    if not isinstance(file, str) :
        return random.choice(files) if len(files) > 0 else DEFAULT_IMAGE_FILE
    
    else :
        return file



def getBoomerAudioFileForFFMPEG(boomer= None, files= []) :
    file = getBoomerAudioFile(boomer)

    if not isinstance(file, str) :
        return random.choice(files) if len(files) > 0 else DEFAULT_AUDIO_FILE
    
    else :
        return file



def getBoomerVideoFileForFFMPEG(boomer= None, files= []) :
    file = getBoomerVideoFile(boomer)

    if not isinstance(file, str) :
        return random.choice(files) if len(files) > 0 else DEFAULT_VIDEO_FILE
    
    else :
        return file






def getBoomerImagePosXForFFMPEG(boomer= None) :
    x = getBoomerImagePosX(boomer)

    if not isinstance(x, str) or x not in list(Position.keys()):
        return DEFAULT_POSITION
    
    else :
        return x
    



def getBoomerImagePosYForFFMPEG(boomer= None) :
    y = getBoomerImagePosY(boomer)

    if not isinstance(y, str) or y not in list(Position.keys()) :
        return DEFAULT_POSITION
   
    else :
        return y    
    


def getBoomerVideoPosXForFFMPEG(boomer= None) :
    x = getBoomerVideoPosX(boomer)

    if not isinstance(x, str) or x not in list(Position.keys()) :
        return DEFAULT_POSITION
    
    else :
        return x
    

def getBoomerVideoPosYForFFMPEG(boomer= None) :
    y = getBoomerVideoPosY(boomer)

    if not isinstance(y, str) or y not in list(Position.keys()) :
        return DEFAULT_POSITION
   
    else :
        return y    





def getBoomerImageMergeStrategyForFFMPEG(boomer= None) :
    ms = getBoomerImageMergeStrategy(boomer)

    if not isinstance(ms, str) or ms not in list(MergeStrategy.keys()) :
        return DEFAULT_IMAGE_MERGESTRATEGY
   
    else :
        return ms
    


def getBoomerVideoMergeStrategyForFFMPEG(boomer= None) :
    ms = getBoomerVideoMergeStrategy(boomer)

    if not isinstance(ms, str) or ms not in list(MergeStrategy.keys()) :
        return DEFAULT_VIDEO_MERGESTRATEGY
   
    else :
        return ms    



def getBoomerImageWidthForFFMPEG(boomer, main_clip_width= 0) :
    w = getBoomerImageWidth(boomer)

    if not isinstance(w, int) or w < MIN_RESOLUTION_SIZE:
        return DEFAULT_IMAGE_WIDTH
    
    elif (main_clip_width + OVERLAY_SIZE_TOLERANCE) < w :
        return main_clip_width + OVERLAY_SIZE_TOLERANCE
       
    else:    
        return abs(w)
    


def getBoomerVideoWidthForFFMPEG(boomer, main_clip_width= 0) :
    w = getBoomerVideoWidth(boomer)

    if not isinstance(w, int) or w < MIN_RESOLUTION_SIZE:
        return DEFAULT_VIDEO_WIDTH
    
    elif (main_clip_width + OVERLAY_SIZE_TOLERANCE) < w :
        return main_clip_width + OVERLAY_SIZE_TOLERANCE

    else:    
        return abs(w)    






def getBoomerImageHeightForFFMPEG(boomer= None, main_clip_height= 0):
    h = getBoomerImageHeight(boomer)

    if not isinstance(h, int) or h < MIN_RESOLUTION_SIZE:
        return main_clip_height
    
    elif (main_clip_height + OVERLAY_SIZE_TOLERANCE) < h:
        return main_clip_height + OVERLAY_SIZE_TOLERANCE
    
    else:    
        return abs(h)    
    



def getBoomerVideoHeightForFFMPEG(boomer= None, main_clip_height= 0):
    h = getBoomerVideoHeight(boomer)

    if not isinstance(h, int) or h < MIN_RESOLUTION_SIZE:
        return main_clip_height
    
    elif (main_clip_height + OVERLAY_SIZE_TOLERANCE) < h:
        return main_clip_height + OVERLAY_SIZE_TOLERANCE
    
    else:    
        return abs(h)    



def getBoomerImageDurationForFFMPEG(boomer= None) :
    dur = getBoomerImageDuration(boomer)

    if not isinstance(dur, int) and not isinstance(dur, float) :
        return 0
    else :
        if dur > MAX_MEDIA_INSERT_DURATION :
            return MAX_MEDIA_INSERT_DURATION
        
        elif dur < MIN_MEDIA_INSERT_DURATION :
            return MIN_MEDIA_INSERT_DURATION
        
        else :
            return abs(dur)



def getBoomerAudioDurationForFFMPEG(boomer= None) :
    dur = getBoomerAudioDuration(boomer)

    if not isinstance(dur, int) and not isinstance(dur, float) :
        return 0
    else :
        if dur > MAX_MEDIA_INSERT_DURATION :
            return MAX_MEDIA_INSERT_DURATION
        
        elif dur < MIN_MEDIA_INSERT_DURATION :
            return MIN_MEDIA_INSERT_DURATION
        
        else :
            return abs(dur)



def getBoomerVideoDurationForFFMPEG(boomer= None) :
    dur = getBoomerVideoDuration(boomer)

    if not isinstance(dur, int) and not isinstance(dur, float) :
        return 0
    
    else :
        if dur > MAX_MEDIA_INSERT_DURATION :
            return MAX_MEDIA_INSERT_DURATION
        
        elif dur < MIN_MEDIA_INSERT_DURATION :
            return MIN_MEDIA_INSERT_DURATION
        
        else :
            return abs(dur)        



def getBoomerBoominTimeForFFMPEG(boomer= None) :
    time = getBoomerBoominTime(boomer)

    if not isinstance(time, int) and not isinstance(time, float) :
        return 0
    else :
        return time



def getBoomerVideoVolumeForFFMPEG(boomer= None) :
    vol = getBoomerVideoVolume(boomer)

    if not isinstance(vol, int) and not isinstance(vol, float) :
        return DEFAULT_VIDEO_VOL
    else :
        if vol > MAX_MEDIA_VOLUME :
            return MAX_MEDIA_VOLUME
        
        elif vol < MIN_MEDIA_VOLUME :
            return MIN_MEDIA_VOLUME
        
        else :
            return abs(vol)
        

def getBoomerAudioVolumeForFFMPEG(boomer= None) :
    vol = getBoomerAudioVolume(boomer)

    if not isinstance(vol, int) and not isinstance(vol, float) :
        return DEFAULT_AUDIO_VOL
    
    else :
        if vol > MAX_MEDIA_VOLUME :
            return MAX_MEDIA_VOLUME
        
        elif vol < MIN_MEDIA_VOLUME :
            return MIN_MEDIA_VOLUME
        
        else :
            return abs(vol)











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

    if not isinstance(trigg, str) or trigg not in list(Trigger.keys()) :
        return DEFAULT_BOOM_TRIGGER
    
    else :
        return Trigger.get(trigg)


def getBoomerBoominTime(boomer= None):
    trigg = getBoomTriggerForFFMPEG(boomer)

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











def getDefaultResoTol(general= None) :
    if (
        not general
    ):
        return None
    
    else:
        return general.get("resotolerance")
    






def getDefaultResoTolForFFMPEG(boomer= None) :
    rt = getDefaultResoTol(boomer)

    if not isinstance(rt, int) and not isinstance(rt, float) :
        return OVERLAY_SIZE_TOLERANCE
   
    else :
        return rt
    

def getDefaultImageDir(boomer= None) :
    if (
        boomer is None
        or boomer.get("image") is None 
    ):
        return None
    
    else:
        return boomer.get("image").get("dir")


def getDefaultAudioDir(boomer= None) :
    if (
        boomer is None
        or boomer.get("audio") is None 
    ):
        return None
    
    else:
        return boomer.get("audio").get("dir")



def getDefaultVideoDir(boomer= None) :
    if (
        boomer is None
        or boomer.get("video") is None 
    ):
        return None
    
    else:
        return boomer.get("video").get("dir")
    




def getBoomerDefaultImageDirForFFMPEG(boomer= None) :
    dir = getDefaultImageDir(boomer)

    if not isinstance(dir, str) or dir not in list(ImageFilesDir.keys()) :
        return DEFAULT_IMAGE_DIR
   
    else :
        return dir



def getBoomerDefaultAudioDirForFFMPEG(boomer= None) :
    dir = getDefaultAudioDir(boomer)

    if not isinstance(dir, str) or dir not in list(AudioFilesDir.keys()) :
        return DEFAULT_AUDIO_DIR
   
    else :
        return dir


def getBoomerDefaultVideoDirForFFMPEG(boomer= None) :
    dir = getDefaultVideoDir(boomer)

    if not isinstance(dir, str) or dir not in list(VideoFilesDir.keys()) :
        return DEFAULT_VIDEO_DIR
   
    else :
        return dir





def getDefaultApiName(general= None) :
    if (
        not general
    ):
        return None
    
    else:
        return general.get("api").get("name")
    









def getDefaultApiNameForFFMPEG(general= None ) :
    name = getDefaultApiName(general)

    if not isinstance(name, str) :
        return DEFAULT_API_NAME
    
    else :
        return name














def getDefaultApiModel(general= None) :
    if (
        not general
    ):
        return DEFAULT_API_MODEL
    
    else:
        return general.get("api").get("model")    









def getDefaultApiModelForFFMPEG(general= None) :
    model = getDefaultApiModel(general)

    if not isinstance(model, str) :
        return DEFAULT_API_MODEL
    
    else :
        return model





















































def as_json_string(value= "") :
    try :
        return '"' + str(value) + '"'
    except :
        return '"null"'

def get_boomer_generator_as_str(generator= None) :
    og_clip = mp.get_og_clip_params()

    addimg = False
    addvid = False
    addaud = False

    if (
        generator is not None
        and generator.get("defaults") is not None
    ) :
        general = generator.get("general")
        default = generator.get("defaults")

        if default.get("image") :
            addimg = True
        if default.get("video") :
            addvid = True
        if default.get("audio") :
            addaud = True                        

        dresotol = getDefaultResoTolForFFMPEG(general)

        dapin = getDefaultApiNameForFFMPEG(general)
        dapim = getDefaultApiModelForFFMPEG(general)

        dbt = getBoomTriggerForFFMPEG(default)

        dimgf = getBoomerImageFile(default)
        imgdir = getBoomerDefaultImageDirForFFMPEG(default)
        dimgms = getBoomerImageMergeStrategyForFFMPEG(default)
        dimgdur = getBoomerImageDurationForFFMPEG(default)
        dimgh = getBoomerImageHeightForFFMPEG(default, og_clip.get("height"))
        dimgw = getBoomerImageWidthForFFMPEG(default, og_clip.get("width"))
        dimgx = getBoomerImagePosXForFFMPEG(default)
        dimgy = getBoomerImagePosYForFFMPEG(default)
        dimgd = getBoomerImageTriggerDelayForFFMPEG(default)

        dvidf = getBoomerVideoFile(default)
        viddir = getBoomerDefaultVideoDirForFFMPEG(default)
        dvidms = getBoomerVideoMergeStrategyForFFMPEG(default)
        dviddur = getBoomerVideoDurationForFFMPEG(default)
        dvidh = getBoomerVideoHeightForFFMPEG(default, og_clip.get("height"))
        dvidw = getBoomerVideoWidthForFFMPEG(default, og_clip.get("width"))
        dvidx = getBoomerVideoPosXForFFMPEG(default)
        dvidy = getBoomerVideoPosYForFFMPEG(default)
        dvidd = getBoomerVideoTriggerDelayForFFMPEG(default)
        dvidvol = getBoomerVideoVolumeForFFMPEG(default)

        daudf = getBoomerAudioFile(default)
        auddir = getBoomerDefaultAudioDirForFFMPEG(default)
        dauddur = getBoomerAudioDurationForFFMPEG(default)
        daudd = getBoomerAudioTriggerDelayForFFMPEG(default)
        daudvol = getBoomerAudioVolumeForFFMPEG(default)

    else :
        addvid = True

        dresotol = variables.OVERLAY_SIZE_TOLERANCE
        dapin = variables.DEFAULT_API_NAME
        dapim = variables.DEFAULT_API_MODEL

        dbt = variables.DEFAULT_BOOM_TRIGGER

        dimgf = variables.DEFAULT_IMAGE_FILE
        imgdir = DEFAULT_IMAGE_DIR        
        dimgms = variables.DEFAULT_IMAGE_MERGE_STRATEGY
        dimgdur = variables.DEFAULT_IMAGE_DURATION
        dimgh = variables.DEFAULT_IMAGE_RESOLUTION_HEIGHT
        dimgw = variables.DEFAULT_IMAGE_RESOLUTION_WIDTH
        dimgx = variables.DEFAULT_IMAGE_POSITION_X
        dimgy = variables.DEFAULT_IMAGE_POSITION_Y
        dimgd = variables.DEFAULT_IMAGE_TRIGGER_DELAY

        dvidf = variables.DEFAULT_VIDEO_FILE
        viddir = DEFAULT_VIDEO_DIR
        dvidms = variables.DEFAULT_VIDEO_MERGE_STRATEGY
        dviddur = variables.DEFAULT_VIDEO_DURATION
        dvidh = variables.DEFAULT_VIDEO_RESOLUTION_HEIGHT
        dvidw = variables.DEFAULT_VIDEO_RESOLUTION_WIDTH
        dvidx = variables.DEFAULT_VIDEO_POSITION_X
        dvidy = variables.DEFAULT_VIDEO_POSITION_Y
        dvidd = variables.DEFAULT_VIDEO_TRIGGER_DELAY
        dvidvol = variables.DEFAULT_VIDEO_VOLUME

        daudf = variables.DEFAULT_AUDIO_FILE
        auddir = DEFAULT_AUDIO_DIR
        dauddur = variables.DEFAULT_AUDIO_DURATION
        daudd = variables.DEFAULT_AUDIO_TRIGGER_DELAY
        daudvol = variables.DEFAULT_AUDIO_VOLUME        


    dresotol = "null" if dresotol is None else as_json_string(dresotol)

    imgdir = "null" if imgdir is None else as_json_string(imgdir)
    auddir = "null" if auddir is None else as_json_string(auddir)
    viddir = "null" if viddir is None else as_json_string(viddir)

    dapin = "null" if dapin is None else as_json_string(dapin)
    dapim = "null" if dapim is None else as_json_string(dapim)

    dbt = "null" if dbt is None else as_json_string(dbt)

    dimgf = "null" if dimgf is None else as_json_string(dimgf)
    dimgms = "null" if dimgms is None else as_json_string(dimgms)
    dimgdur = "null" if dimgdur is None else dimgdur               
    dimgh = "null" if dimgh is None else dimgh                     
    dimgw = "null" if dimgw is None else dimgw                     
    dimgx = "null" if dimgx is None else as_json_string(dimgx)
    dimgy = "null" if dimgy is None else as_json_string(dimgy)
    dimgd = "null" if dimgd is None else dimgd

    dvidf = "null" if dvidf is None else as_json_string(dvidf)
    dvidms = "null" if dvidms is None else as_json_string(dvidms)
    dviddur = "null" if dviddur is None else dviddur               
    dvidh = "null" if dvidh is None else dvidh                     
    dvidw = "null" if dvidw is None else dvidw                     
    dvidx = "null" if dvidx is None else as_json_string(dvidx)
    dvidy = "null" if dvidy is None else as_json_string(dvidy)
    dvidd = "null" if dvidd is None else dvidd
    dvidvol = "null" if dvidvol is None else dvidvol               

    daudf = "null" if daudf is None else as_json_string(daudf)
    dauddur = "null" if dauddur is None else dauddur               
    daudd = "null" if daudd is None else daudd
    daudvol = "null" if daudvol is None else daudvol
    
    if addimg :
        imagedefaults = ( 
f"""
                        "image": {{
                            "file": {dimgf},
                            "dir": {imgdir},                    
                            "conf": {{
                                "mergestrategy": {dimgms},
                                "duration": {dimgdur},
                                "height": {dimgh},
                                "width": {dimgw},               
                                "posx": {dimgx},
                                "posy": {dimgy},
                                "triggerdelay": {dimgd}
                            }}

                        }}""")
    else :
        imagedefaults = ""

    if addvid :
        videodefaults = ( 
f"""
                        "video": {{
                            "file": {dvidf},
                            "dir": {viddir},                    
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
                        }}""")
    else :
        videodefaults = ""

    if addaud :
        audiodefaults = ( 
f"""
                        "audio": {{
                            "file": {daudf},
                            "dir": {auddir},                    
                            "conf": {{
                                "duration": {dauddur},
                                "triggerdelay": {daudd},
                                "volume": {daudvol}
                            }}
                        }}
""")
    else :
        audiodefaults = ""


    imgvidseparator = ",\n" if addimg and (addvid or addaud) else ""
    vidaudseparator = ",\n" if addvid and addaud else ""



    return f""" {{
                    "general": {{
                        "resotolerance": {dresotol},
                        
                        "audiodir": {auddir},
                        "videodir": {viddir},
                        
                        "api": {{
                            "name": {dapin},
                            "model": {dapim}
                        }}
                    }},

                    "defaults": {{
                        "word": {{
                            "trigger": {dbt}
                        }},

                        {imagedefaults + imgvidseparator}

                        {videodefaults + vidaudseparator}

                        {audiodefaults}

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

    if default.get("image") is not None :
        obj["image"] = {
            "file": getBoomerImageFileForFFMPEG(default, image_files),
            "dir": getBoomerDefaultImageDirForFFMPEG(default),
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
    else :
        obj["image"] = None

    if default.get("audio") is not None :
        obj["audio"] = {
            "file": getBoomerAudioFileForFFMPEG(default, audio_files),
            "dir": getBoomerDefaultAudioDirForFFMPEG(default),            
            "conf": {
                "duration": getBoomerAudioDuration(default),
                "triggerdelay": getBoomerAudioTriggerDelay(default),
                "volume": getBoomerAudioVolume(default)
            }
        }
    else :
        obj["audio"] = None

    if default.get("video") is not None :
        obj["video"] = {
            "file": getBoomerVideoFileForFFMPEG(default, video_files),
            "dir": getBoomerDefaultVideoDirForFFMPEG(default),            
            "conf": {
                "mergestrategy": getBoomerVideoMergeStrategy(default),
                "duration": getBoomerVideoDuration(default),
                "height": getBoomerVideoHeight(default),
                "width": getBoomerVideoWidth(default),
                "posx": getBoomerVideoPosX(default),
                "posy": getBoomerVideoPosY(default),
                "triggerdelay": getBoomerVideoTriggerDelay(default),
                "volume": getBoomerVideoVolume(default)
            }
        }
    else :
        obj["video"] = None


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
