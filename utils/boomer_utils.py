import json
import requests
import random

from .settings import variables
from .enum.Enum import MergeStrategy, Trigger, Position, ImageFilesDir, VideoFilesDir, AudioFilesDir
from . import moviepy_utils as mp




DEFAULT_BOOMIN_TIME = variables.DEFAULT_BOOMIN_TIME
DEFAULT_VIDEO_DURATION = variables.DEFAULT_VIDEO_DURATION
DEFAULT_AUDIO_DURATION = variables.DEFAULT_AUDIO_DURATION
DEFAULT_IMAGE_DURATION = variables.DEFAULT_IMAGE_DURATION
DEFAULT_IMAGE_DIR = variables.DEFAULT_IMAGE_DIR
DEFAULT_AUDIO_DIR = variables.DEFAULT_AUDIO_DIR
DEFAULT_VIDEO_DIR = variables.DEFAULT_VIDEO_DIR
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
        strategy = getBoomerImageParamMergeStrategyForFFMPEG(b)

        if strategy == MergeStrategy.get("COMPOSE") :

            image_files_compose = image_files_compose + [b]
        elif strategy == MergeStrategy.get("CONCAT") :

            image_files_concat = image_files_concat + [b]

    return (image_files_compose, image_files_concat)





def get_fake_boomers_for_video_params_concat(boomers= []) :
    video_files_concat = []

    for b in boomers:
        video_params = [param for param in b.get("video")] if b.get("video") else []

        for param in video_params :
            strategy = getBoomerVideoParamMergeStrategyForFFMPEG(param)

            if strategy == MergeStrategy.get("CONCAT") :
                param["word"] = b.get("word")
                video_files_concat = video_files_concat + [param]

    return video_files_concat





def get_fake_boomers_for_video_params_compose(boomers= []) :
    video_files_compose = []

    for b in boomers:
        video_params = [param for param in b.get("video")] if b.get("video") else []

        for param in video_params :
            strategy = getBoomerVideoParamMergeStrategyForFFMPEG(param)

            if strategy == MergeStrategy.get("COMPOSE") :
                param["word"] = b.get("word")
                video_files_compose = video_files_compose + [param]

    return video_files_compose





def get_fake_boomers_for_image_params_compose(boomers= []) :
    image_files_compose = []

    for b in boomers:
        image_params = [param for param in b.get("image")] if b.get("image") else []

        for param in image_params :
            strategy = getBoomerImageParamMergeStrategyForFFMPEG(param)

            if strategy == MergeStrategy.get("COMPOSE") :
                param["word"] = b.get("word")
                image_files_compose = image_files_compose + [param]

    return image_files_compose



def get_fake_boomers_for_image_params_concat(boomers= []) :
    image_files_concat = []

    for b in boomers:
        image_params = [param for param in b.get("image")] if b.get("image") else []

        for param in image_params :
            strategy = getBoomerImageParamMergeStrategyForFFMPEG(param)

            if strategy == MergeStrategy.get("CONCAT") :
                param["word"] = b.get("word")
                image_files_concat = image_files_concat + [param]

    return image_files_concat



def get_fake_boomers_for_audio_params(boomers= []) :
    audio_files_concat = []

    for b in boomers:
        audio_params = [param for param in b.get("audio")] if b.get("audio") else []

        for param in audio_params :
            param["word"] = b.get("word")
            audio_files_concat = audio_files_concat + [param]

    return audio_files_concat






def classifyBoomersByVideoMergeStrategy(boomers= []):
    video_files_compose = []
    video_files_concat = []

    for b in boomers:
        strategy = getBoomerVideoParamMergeStrategyForFFMPEG(b)

        if strategy == MergeStrategy.get("COMPOSE") :

            video_files_compose = video_files_compose + [b]
        elif strategy == MergeStrategy.get("CONCAT") :

            video_files_concat = video_files_concat + [b]

    return (video_files_compose, video_files_concat)







def filterBoomers(og_clip_duration= 0, boomers= []):
    out_of_bounds_boomers_bot = []
    regular_boomers = []
    out_of_bounds_boomers_top = []

    boomers.sort(key= getBoomerBoominTimeForFFMPEG)

    for boomer in boomers:
        boomin_time = getBoomerBoominTimeForFFMPEG(boomer)
        if boomin_time > 0 and boomin_time < og_clip_duration:
            regular_boomers = regular_boomers + [boomer]
        elif boomin_time <= 0:
            boomer["word"] = { "content": "", "start": 0, "end": 0, "trigger": "start"}
            out_of_bounds_boomers_bot = out_of_bounds_boomers_bot + [boomer]
        elif boomin_time >= og_clip_duration:
            boomer["word"] = { "content": "", "start": og_clip_duration, "end": og_clip_duration, "trigger": "start" }            
            out_of_bounds_boomers_top = out_of_bounds_boomers_top + [boomer]

    return (out_of_bounds_boomers_top, regular_boomers, out_of_bounds_boomers_bot)







def get_sojufile_from_path(path= None) :
    if not path :
        return None
    
    with open(path, 'r') as file :
        return json.load(file).get("soju")





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
    try :
        response = requests.get(jsonfilepath)
        data = "{}"

        if (response.status_code):
            data = response.text
    
        content = json.loads(data).get("soju")
        return content
    
    except :
        return {}
    





























def getBoomerAudioParamTriggerDelayForFFMPEG(param= None) :
    td = getBoomerAudioParamTriggerDelay(param)

    if not isinstance(td, int) and not isinstance(td, float) :
        return DEFAULT_DELAY
    
    else :
        if td > MAX_MEDIA_DELAY :
            return MAX_MEDIA_DELAY
        
        elif td < MIN_MEDIA_DELAY :
            return MIN_MEDIA_DELAY
        
        else :
            return abs(td)

def getBoomerAudioParamTriggerDelayForSojufile(param= None) :
    td = getBoomerAudioParamTriggerDelay(param)

    if not isinstance(td, int) and not isinstance(td, float) :
        return None
    
    else :
        if td > MAX_MEDIA_DELAY :
            return MAX_MEDIA_DELAY
        
        elif td < MIN_MEDIA_DELAY :
            return MIN_MEDIA_DELAY
        
        else :
            return abs(td)



def getBoomerVideoParamTriggerDelayForFFMPEG(param= None) :
    td = getBoomerVideoParamTriggerDelay(param)

    if not isinstance(td, int) and not isinstance(td, float) :
        return DEFAULT_DELAY
    
    else :
        if td > MAX_MEDIA_DELAY :
            return MAX_MEDIA_DELAY
        
        elif td < MIN_MEDIA_DELAY :
            return MIN_MEDIA_DELAY
        
        else :
            return abs(td)


def getBoomerVideoParamTriggerDelayForSojufile(param= None) :
    td = getBoomerVideoParamTriggerDelay(param)

    if not isinstance(td, int) and not isinstance(td, float) :
        return None
    
    else :
        if td > MAX_MEDIA_DELAY :
            return MAX_MEDIA_DELAY
        
        elif td < MIN_MEDIA_DELAY :
            return MIN_MEDIA_DELAY
        
        else :
            return abs(td)




def getBoomerImageParamTriggerDelayForFFMPEG(param= None) :
    td = getBoomerImageParamTriggerDelay(param)

    if not isinstance(td, int) and not isinstance(td, float) :
        return DEFAULT_DELAY
    
    else :
        if td > MAX_MEDIA_DELAY :
            return MAX_MEDIA_DELAY
        
        elif td < MIN_MEDIA_DELAY :
            return MIN_MEDIA_DELAY
        
        else :
            return abs(td)

def getBoomerImageParamTriggerDelayForSojufile(param= None) :
    td = getBoomerImageParamTriggerDelay(param)

    if not isinstance(td, int) and not isinstance(td, float) :
        return None
    
    else :
        if td > MAX_MEDIA_DELAY :
            return MAX_MEDIA_DELAY
        
        elif td < MIN_MEDIA_DELAY :
            return MIN_MEDIA_DELAY
        
        else :
            return abs(td)



def getBoomerImageParamFileForFFMPEG(param= None, files= []) :
    file = getBoomerImageParamFile(param)

    if not isinstance(file, str) :
        return random.choice(files) if files else DEFAULT_IMAGE_FILE
    
    else :
        return file



def getBoomerAudioParamFileForFFMPEG(param= None, files= []) :
    file = getBoomerAudioParamFile(param)

    if not isinstance(file, str) :
        return random.choice(files) if files else DEFAULT_AUDIO_FILE
    
    else :
        return file



def getBoomerVideoParamFileForFFMPEG(param= None, files= []) :
    file = getBoomerVideoParamFile(param)

    if not isinstance(file, str) :
        return random.choice(files) if files else DEFAULT_VIDEO_FILE
    
    else :
        return file






def getBoomerImageParamPosXForFFMPEG(param= None) :
    x = getBoomerImageParamPosX(param)

    if not isinstance(x, str) or x not in list(Position.keys()):
        return DEFAULT_POSITION
    
    else :
        return Position.get(x)


def getBoomerImageParamPosYForFFMPEG(param= None) :
    y = getBoomerImageParamPosY(param)

    if not isinstance(y, str) or y not in list(Position.keys()) :
        return DEFAULT_POSITION
   
    else :
        return Position.get(y)     
    
def getBoomerImageParamPosXForSojufile(param= None) :
    x = getBoomerImageParamPosX(param)

    if not isinstance(x, str) or x not in list(Position.keys()):
        return None
    
    else :
        return Position.get(x)


def getBoomerImageParamPosYForSojufile(param= None) :
    y = getBoomerImageParamPosY(param)

    if not isinstance(y, str) or y not in list(Position.keys()) :
        return None
   
    else :
        return Position.get(y)     




def getBoomerVideoParamPosXForFFMPEG(param= None) :
    x = getBoomerVideoParamPosX(param)

    if not isinstance(x, str) or x not in list(Position.keys()) :
        return DEFAULT_POSITION
    
    else :
        return Position.get(x)
    

def getBoomerVideoParamPosYForFFMPEG(param= None) :
    y = getBoomerVideoParamPosY(param)

    if not isinstance(y, str) or y not in list(Position.keys()) :
        return DEFAULT_POSITION
   
    else :
        return Position.get(y)    

def getBoomerVideoParamPosXForSojufile(param= None) :
    x = getBoomerVideoParamPosX(param)

    if not isinstance(x, str) or x not in list(Position.keys()) :
        return None
    
    else :
        return Position.get(x)
    

def getBoomerVideoParamPosYForSojufile(param= None) :
    y = getBoomerVideoParamPosY(param)

    if not isinstance(y, str) or y not in list(Position.keys()) :
        return None
   
    else :
        return Position.get(y)    






def getBoomerImageParamMergeStrategyForFFMPEG(param= None) :
    ms = getBoomerImageParamMergeStrategy(param)

    if not isinstance(ms, str) or ms not in list(MergeStrategy.keys()) :
        return DEFAULT_IMAGE_MERGESTRATEGY
   
    else :
        return MergeStrategy.get(ms)
    
def getBoomerImageParamMergeStrategyForSojufile(param= None) :
    ms = getBoomerImageParamMergeStrategy(param)

    if not isinstance(ms, str) or ms not in list(MergeStrategy.keys()) :
        return None
   
    else :
        return MergeStrategy.get(ms)



def getBoomerVideoParamMergeStrategyForFFMPEG(param= None) :
    ms = getBoomerVideoParamMergeStrategy(param)

    if not isinstance(ms, str) or ms not in list(MergeStrategy.keys()) :
        return DEFAULT_VIDEO_MERGESTRATEGY
   
    else :
        return MergeStrategy.get(ms)    

def getBoomerVideoParamMergeStrategyForSojufile(param= None) :
    ms = getBoomerVideoParamMergeStrategy(param)

    if not isinstance(ms, str) or ms not in list(MergeStrategy.keys()) :
        return None
   
    else :
        return MergeStrategy.get(ms)    




def getBoomerImageParamWidthForFFMPEG(param, main_clip_width= 0) :
    w = getBoomerImageParamWidth(param)

    if not isinstance(w, int) or w < MIN_RESOLUTION_SIZE:
        return DEFAULT_IMAGE_WIDTH
    
    elif (main_clip_width + OVERLAY_SIZE_TOLERANCE) < w :
        return main_clip_width + OVERLAY_SIZE_TOLERANCE
       
    else:    
        return abs(w)
    
def getBoomerImageParamWidthForSojufile(param, main_clip_width= 0) :
    w = getBoomerImageParamWidth(param)

    if not isinstance(w, int) or w < MIN_RESOLUTION_SIZE:
        return None
    
    elif (main_clip_width + OVERLAY_SIZE_TOLERANCE) < w :
        return main_clip_width + OVERLAY_SIZE_TOLERANCE
       
    else:    
        return abs(w)



def getBoomerVideoParamWidthForFFMPEG(param, main_clip_width= 0) :
    w = getBoomerVideoParamWidth(param)

    if not isinstance(w, int) or w < MIN_RESOLUTION_SIZE:
        return DEFAULT_VIDEO_WIDTH
    
    elif (main_clip_width + OVERLAY_SIZE_TOLERANCE) < w :
        return main_clip_width + OVERLAY_SIZE_TOLERANCE

    else:    
        return abs(w)    

def getBoomerVideoParamWidthForSojufile(param, main_clip_width= 0) :
    w = getBoomerVideoParamWidth(param)

    if not isinstance(w, int) or w < MIN_RESOLUTION_SIZE:
        return None
    
    elif (main_clip_width + OVERLAY_SIZE_TOLERANCE) < w :
        return main_clip_width + OVERLAY_SIZE_TOLERANCE

    else:    
        return abs(w)    




def getBoomerImageParamHeightForFFMPEG(param= None, main_clip_height= 0):
    h = getBoomerImageParamHeight(param)

    if not isinstance(h, int) or h < MIN_RESOLUTION_SIZE:
        return main_clip_height
    
    elif (main_clip_height + OVERLAY_SIZE_TOLERANCE) < h:
        return main_clip_height + OVERLAY_SIZE_TOLERANCE
    
    else:    
        return abs(h)    
    
def getBoomerImageParamHeightForSojufile(param= None, main_clip_height= 0):
    h = getBoomerImageParamHeight(param)

    if not isinstance(h, int) or h < MIN_RESOLUTION_SIZE:
        return None
    
    elif (main_clip_height + OVERLAY_SIZE_TOLERANCE) < h:
        return main_clip_height + OVERLAY_SIZE_TOLERANCE
    
    else:    
        return abs(h)    



def getBoomerVideoParamHeightForFFMPEG(param= None, main_clip_height= 0):
    h = getBoomerVideoParamHeight(param)

    if not isinstance(h, int) or h < MIN_RESOLUTION_SIZE:
        return main_clip_height
    
    elif (main_clip_height + OVERLAY_SIZE_TOLERANCE) < h:
        return main_clip_height + OVERLAY_SIZE_TOLERANCE
    
    else:    
        return abs(h)    
    
def getBoomerVideoParamHeightForSojufile(param= None, main_clip_height= 0):
    h = getBoomerVideoParamHeight(param)

    if not isinstance(h, int) or h < MIN_RESOLUTION_SIZE:
        return None
    
    elif (main_clip_height + OVERLAY_SIZE_TOLERANCE) < h:
        return main_clip_height + OVERLAY_SIZE_TOLERANCE
    
    else:    
        return abs(h)        



def getBoomerImageParamDurationForFFMPEG(param= None) :
    dur = getBoomerImageParamDuration(param)

    if not isinstance(dur, int) and not isinstance(dur, float) :
        return DEFAULT_IMAGE_DURATION
    else :
        if dur > MAX_MEDIA_INSERT_DURATION :
            return MAX_MEDIA_INSERT_DURATION
        
        elif dur < MIN_MEDIA_INSERT_DURATION :
            return MIN_MEDIA_INSERT_DURATION
        
        else :
            return abs(dur)

def getBoomerImageParamDurationForSojufile(param= None) :
    dur = getBoomerImageParamDuration(param)

    if not isinstance(dur, int) and not isinstance(dur, float) :
        return None
    else :
        if dur > MAX_MEDIA_INSERT_DURATION :
            return MAX_MEDIA_INSERT_DURATION
        
        elif dur < MIN_MEDIA_INSERT_DURATION :
            return MIN_MEDIA_INSERT_DURATION
        
        else :
            return abs(dur)



def getBoomerAudioParamDurationForFFMPEG(param= None) :
    dur = getBoomerAudioParamDuration(param)

    if not isinstance(dur, int) and not isinstance(dur, float) :
        return DEFAULT_AUDIO_DURATION
    else :
        if dur > MAX_MEDIA_INSERT_DURATION :
            return MAX_MEDIA_INSERT_DURATION
        
        elif dur < MIN_MEDIA_INSERT_DURATION :
            return MIN_MEDIA_INSERT_DURATION
        
        else :
            return abs(dur)

def getBoomerAudioParamDurationForSojufile(param= None) :
    dur = getBoomerAudioParamDuration(param)

    if not isinstance(dur, int) and not isinstance(dur, float) :
        return None
    else :
        if dur > MAX_MEDIA_INSERT_DURATION :
            return MAX_MEDIA_INSERT_DURATION
        
        elif dur < MIN_MEDIA_INSERT_DURATION :
            return MIN_MEDIA_INSERT_DURATION
        
        else :
            return abs(dur)



def getBoomerVideoParamDurationForFFMPEG(param= None) :
    dur = getBoomerVideoParamDuration(param)

    if not isinstance(dur, int) and not isinstance(dur, float) :
        return DEFAULT_VIDEO_DURATION
    
    else :
        if dur > MAX_MEDIA_INSERT_DURATION :
            return MAX_MEDIA_INSERT_DURATION
        
        elif dur < MIN_MEDIA_INSERT_DURATION :
            return MIN_MEDIA_INSERT_DURATION
        
        else :
            return abs(dur)        

def getBoomerVideoParamDurationForSojufile(param= None) :
    dur = getBoomerVideoParamDuration(param)

    if not isinstance(dur, int) and not isinstance(dur, float) :
        return None
    
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
        return DEFAULT_BOOMIN_TIME
    else :
        return time



def getBoomerVideoParamVolumeForFFMPEG(param= None) :
    vol = getBoomerVideoParamVolume(param)

    if not isinstance(vol, int) and not isinstance(vol, float) :
        return DEFAULT_VIDEO_VOL
    else :
        if vol > MAX_MEDIA_VOLUME :
            return MAX_MEDIA_VOLUME
        
        elif vol < MIN_MEDIA_VOLUME :
            return MIN_MEDIA_VOLUME
        
        else :
            return abs(vol)
        

def getBoomerVideoParamVolumeForSojufile(param= None) :
    vol = getBoomerVideoParamVolume(param)

    if not isinstance(vol, int) and not isinstance(vol, float) :
        return None
    else :
        if vol > MAX_MEDIA_VOLUME :
            return MAX_MEDIA_VOLUME
        
        elif vol < MIN_MEDIA_VOLUME :
            return MIN_MEDIA_VOLUME
        
        else :
            return abs(vol)

        

def getBoomerAudioParamVolumeForFFMPEG(param= None) :
    vol = getBoomerAudioParamVolume(param)

    if not isinstance(vol, int) and not isinstance(vol, float) :
        return DEFAULT_AUDIO_VOL
    
    else :
        if vol > MAX_MEDIA_VOLUME :
            return MAX_MEDIA_VOLUME
        
        elif vol < MIN_MEDIA_VOLUME :
            return MIN_MEDIA_VOLUME
        
        else :
            return abs(vol)


def getBoomerAudioParamVolumeForSojufile(param= None) :
    vol = getBoomerAudioParamVolume(param)

    if not isinstance(vol, int) and not isinstance(vol, float) :
        return None
    
    else :
        if vol > MAX_MEDIA_VOLUME :
            return MAX_MEDIA_VOLUME
        
        elif vol < MIN_MEDIA_VOLUME :
            return MIN_MEDIA_VOLUME
        
        else :
            return abs(vol)










def getBoomerImageParamWidth(param= None):
    if (
        param is None
    ):
        return None
    
    else:    
        return param.get("width")
    







def getBoomerImageParamHeight(param= None):
    if (
        param is None
    ):
        return None
    
    else:    
        return param.get("height")    
    







def getBoomerVideoParamWidth(param= None):
    if (
        param is None
    ):
        return None
    
    else:    
        return param.get("width")
    





def getBoomerVideoParamHeight(param= None):
    if (
        param is None
    ):
        return None
    
    else:    
        return param.get("height")    







def getBoomTrigger(boomer= None):
    if (
        boomer is None
        or boomer.get("word") is None
    ):
        return None
    
    else:
        return boomer.get("word").get("trigger")






def getBoomTriggerForFFMPEG(boomer= None) :
    trigg = getBoomTrigger(boomer)

    if trigg not in list(Trigger.keys()) :
        return DEFAULT_BOOM_TRIGGER
    
    else :
        return Trigger.get(trigg)
    
def getBoomTriggerForSojufile(boomer= None) :
    trigg = getBoomTrigger(boomer)

    if trigg not in list(Trigger.keys()) :
        return None
    
    else :
        return Trigger.get(trigg)    


def getBoomerBoominTime(boomer= None):
    trigg = getBoomTriggerForFFMPEG(boomer)

    if (
        boomer is None
        or trigg is None
        or boomer.get("word") is None
        or boomer.get("word").get(trigg) is None
    ):
        return None
    
    else:
        return float(boomer.get("word").get(trigg))



def getBoomWordContentForSojufile(boomer= None) :
    if (
        boomer is None
        or boomer.get("word") is None
        or boomer.get("word").get("content") is None
    ):
        return None
    
    else:
        return boomer.get("word").get("content")









def getBoomerImageParamDuration(param= None):
    if (
        param is None 
    ):
        return None
    
    else:
        return param.get("duration")








def getBoomerAudioParamDuration(param= None):
    if (
        param is None 
    ):
        return None
    
    else:
        return param.get("duration")
    






def getBoomerVideoParamDuration(param= None):
    if (
        param is None 
    ):
        return None
    
    else:
        return param.get("duration")











def getBoomerVideoParamVolume(param= None):
    if (
        param is None
    ):
        return None

    else:
        return param.get("volume")
    







def getBoomerAudioParamVolume(param= None):
    if (
        param is None
    ):
        return None

    else:
        return param.get("volume")    









def getBoomerImageParamFile(param= None) :
    if (
        param is None
    ):
        return None
    
    else:
        return param.get("file")






def getBoomerAudioParamFile(param= None) :
    if (
        param is None 
    ):
        return None
    
    else:
        return param.get("file")










def getBoomerVideoParamFile(param= None) :
    if (
        param is None
    ):
        return None
    
    else:
        return param.get("file")








def getBoomerImageParamMergeStrategy(param= None) :
    if (
        param is None
    ):
        return None
    
    else:
        return param.get("mergestrategy")








def getBoomerVideoParamMergeStrategy(param= None) :
    if (
        param is None
    ):
        return None
    
    else:
        return param.get("mergestrategy")











def getBoomerImageParamPosX(param= None) :
    if (
        param is None
    ):
        return None
    
    else:
        return param.get("posx")



def getBoomerImageParamPosY(param= None) :
    if (
        param is None
    ):
        return None
    
    else:
        return param.get("posy")




def getBoomerVideoParamPosX(param= None) :
    if (
        param is None
    ):
        return None
    
    else:
        return param.get("posx")



def getBoomerVideoParamPosY(param= None) :
    if (
        param is None
    ):
        return None
    
    else:
        return param.get("posy")





def getBoomerImageParamTriggerDelay(param= None) :
    if (
        param is None
    ):
        return None
    
    else:
        return param.get("triggerdelay")




def getBoomerVideoParamTriggerDelay(param= None) :
    if (
        param is None
    ):
        return None
    
    else:
        return param.get("triggerdelay")








def getBoomerAudioParamTriggerDelay(param= None) :
    if (
        param is None
    ):
        return None
    
    else:
        return param.get("triggerdelay")











    

def getBoomerImageParamDir(param= None) :
    if (
        param is None
    ):
        return None
    
    else:
        return param.get("dir")


def getBoomerAudioParamDir(param= None) :
    if (
        param is None 
    ):
        return None
    
    else:
        return param.get("dir")



def getBoomerVideoParamDir(param= None) :
    if (
        param is None
    ):
        return None
    
    else:
        return param.get("dir")
    




def getBoomerImageParamDirForFFMPEG(param= None) :
    dir = getBoomerImageParamDir(param)

    if not isinstance(dir, str) or dir not in list(ImageFilesDir.keys()) :
        return DEFAULT_IMAGE_DIR
   
    else :
        return dir

def getBoomerImageParamDirForSojufile(param= None) :
    dir = getBoomerImageParamDir(param)

    if not isinstance(dir, str) or dir not in list(ImageFilesDir.keys()) :
        if not isinstance(dir, int) :
            return None
        else :
            return dir
   
    else :
        return dir


def getBoomerAudioParamDirForFFMPEG(param= None) :
    dir = getBoomerAudioParamDir(param)

    if not isinstance(dir, str) or dir not in list(AudioFilesDir.keys()) :
        return DEFAULT_AUDIO_DIR
   
    else :
        return dir
    
def getBoomerAudioParamDirForSojufile(param= None) :
    dir = getBoomerAudioParamDir(param)

    if not isinstance(dir, str) or dir not in list(AudioFilesDir.keys()) :
        if not isinstance(dir, int) :
            return None
        else :
            return dir
   
    else :
        return dir



def getBoomerVideoParamDirForFFMPEG(param= None) :
    dir = getBoomerVideoParamDir(param)

    if not isinstance(dir, str) or dir not in list(VideoFilesDir.keys()) :
        return DEFAULT_VIDEO_DIR
   
    else :
        return dir


def getBoomerVideoParamDirForSojufile(param= None) :
    dir = getBoomerVideoParamDir(param)

    if not isinstance(dir, str) or dir not in list(VideoFilesDir.keys()) :
        if not isinstance(dir, int) :
            return None
        else :
            return dir
   
    else :
        return dir





def getGeneralsApiName(api= None) :
    if (
        api is None
    ):
        return None
    
    else:
        return api.get("name")
    


def getGeneralsApiModel(api= None) :
    if (
        api is None
    ):
        return None
    
    else:
        return api.get("model")    
    




























def build_sojufile_for_discord(outputname= "sojufile.soju.json", boomers= []) :

        with open(outputname, 'w') as f :
            f.writelines(
f"""
{{
\t"soju": {{
     
\t\t"boomers": [

\t\t],

\t\t"generated": [
"""
            )
            
            for i, boomer in enumerate(boomers):
                word = ('\t\t\t\t"word": ' +  json.dumps(boomer.get("word"))) if boomer.get("word") else ""
                image = (',\n\t\t\t\t"image": ' +  json.dumps(boomer.get("image"))) if boomer.get("image") else ""
                audio = (',\n\t\t\t\t"audio": ' +  json.dumps(boomer.get("audio"))) if boomer.get("audio") else ""
                video = (',\n\t\t\t\t"video": ' +  json.dumps(boomer.get("video"))) if boomer.get("video") else ""
                comma = ',' if i < (len(boomers) - 1) else ''


                f.writelines(f"""
\t\t\t{{
{word}{image}{audio}{video}
\t\t\t}}{comma}
""")

            f.writelines(
"""
\t\t]

\t}
}            
"""         )

        
        return outputname




















def prepare_boomer_gen_gens_api(api= None) :
    healthy_api = {}

    if type(api) is dict :
        healthy_api["name"] = getGeneralsApiName(api)
        healthy_api["model"] = getGeneralsApiModel(api)
    
    else :
        dgenerator = open("./assets/json/dgenerator.soju.json")
        healthy_api = json.load(dgenerator)["soju"]["generator"].get("generals").get("api")

    return healthy_api
        



def prepare_boomer_gen_generals(generals= None) :
    healthy_generals = {}

    if type(generals) is dict :
        healthy_generals["api"] = prepare_boomer_gen_gens_api(generals.get("api"))
    
    else :
        dgenerator = open("./assets/json/dgenerator.soju.json")
        healthy_generals = json.load(dgenerator)["soju"]["generator"].get("generals")

    return healthy_generals



def prepare_boomer_gen_defaults(boomer= None) :
    healthy_defaults = {}

    og_clip = mp.get_og_clip_params()


    if type(boomer) is dict :
        boomer_word = {}
        if type(boomer.get("word")) is dict :
                boomer_word["content"] = getBoomWordContentForSojufile(boomer)
                boomer_word["trigger"] = getBoomTriggerForSojufile(boomer)

        boomer_image = []
        if type(boomer.get("image")) is list :
            for img_param in boomer.get("image"):
                new_param = {}
                
                new_param["file"] = getBoomerImageParamFile(img_param)
                new_param["dir"] = getBoomerImageParamDirForSojufile(img_param)
                new_param["mergestrategy"] = getBoomerImageParamMergeStrategyForSojufile(img_param)
                new_param["duration"] = getBoomerImageParamDurationForSojufile(img_param)
                new_param["height"] = getBoomerImageParamHeightForSojufile(img_param, og_clip.get("height"))
                new_param["width"] = getBoomerImageParamWidthForSojufile(img_param, og_clip.get("width"))
                new_param["posx"] = getBoomerImageParamPosXForSojufile(img_param)
                new_param["posy"] = getBoomerImageParamPosYForSojufile(img_param)
                new_param["triggerdelay"] = getBoomerImageParamTriggerDelayForSojufile(img_param)

                boomer_image = boomer_image + [new_param]

        boomer_video = []
        if type(boomer.get("video")) is list :
            for vid_param in boomer.get("video"):
                new_param = {}
                
                new_param["file"] = getBoomerVideoParamFile(vid_param)
                new_param["dir"] = getBoomerVideoParamDirForSojufile(vid_param)
                new_param["mergestrategy"] = getBoomerVideoParamMergeStrategyForSojufile(vid_param)
                new_param["duration"] = getBoomerVideoParamDurationForSojufile(vid_param)
                new_param["height"] = getBoomerVideoParamHeightForSojufile(vid_param, og_clip.get("height"))
                new_param["width"] = getBoomerVideoParamWidthForSojufile(vid_param, og_clip.get("width"))
                new_param["posx"] = getBoomerVideoParamPosXForSojufile(vid_param)
                new_param["posy"] = getBoomerVideoParamPosYForSojufile(vid_param)
                new_param["triggerdelay"] = getBoomerVideoParamTriggerDelayForSojufile(vid_param)
                new_param["volume"] = getBoomerVideoParamVolumeForSojufile(vid_param)

                boomer_video = boomer_video + [new_param]

        boomer_audio = []
        if type(boomer.get("audio")) is list :
            for aud_param in boomer.get("audio"):
                new_param = {}

                new_param["file"] = getBoomerAudioParamFile(aud_param)
                new_param["dir"] = getBoomerAudioParamDirForSojufile(aud_param)
                new_param["duration"] = getBoomerAudioParamDurationForSojufile(aud_param)
                new_param["triggerdelay"] = getBoomerAudioParamTriggerDelayForSojufile(aud_param)
                new_param["volume"] = getBoomerAudioParamVolumeForSojufile(aud_param)

                boomer_audio = boomer_audio + [new_param]

        if boomer_word :
            healthy_defaults["word"] = boomer_word
        if boomer_image :
            healthy_defaults["image"] = boomer_image
        if boomer_video :
            healthy_defaults["video"] = boomer_video
        if boomer_audio :            
            healthy_defaults["audio"] = boomer_audio
    else :
        dgenerator = open("./assets/json/dgenerator.soju.json")
        healthy_defaults = json.load(dgenerator)["soju"]["generator"].get("defaults")                  

    return healthy_defaults


def as_json_string(value= "") :
    try :
        return '"' + value + '"'
    except :
        return "null"
    
def as_json_float(value= "") :
    try :
        return float(value)
    except :
        return None
    
def as_json_int(value= "") :
    try :
        return int(float(value))
    except :
        return None    


def prepare_boomer_generator(generator= None) :
    healthy_generator = {}

    if type(generator) is dict :
        healthy_generator["generals"] = prepare_boomer_gen_generals(generator.get("generals"))
        healthy_generator["defaults"] = prepare_boomer_gen_defaults(generator.get("defaults"))
    else :
        dgenerator = open("./assets/json/dgenerator.soju.json")
        healthy_generator = json.load(dgenerator).get("soju").get("generator")
        
    return healthy_generator




def create_boomer_generator_as_str(generator= None) :
    og_clip = mp.get_og_clip_params()

    addimg = False
    addvid = False
    addaud = False

    if (
        generator is not None
        and generator.get("defaults") is not None
    ) :
        general = generator.get("generals")
        default = generator.get("defaults")

        dbt = getBoomTriggerForSojufile(default)

        if type(default.get("image")) is list :
            addimg = True

            boomer_image = []
            for img_param in default.get("image"):
                new_param = {}
                
                new_param["file"] = getBoomerImageParamFile(img_param)
                new_param["dir"] = getBoomerImageParamDirForSojufile(img_param)
                new_param["mergestrategy"] = getBoomerImageParamMergeStrategyForSojufile(img_param)
                new_param["duration"] = getBoomerImageParamDurationForSojufile(img_param)
                new_param["height"] = getBoomerImageParamHeightForSojufile(img_param, og_clip.get("height"))
                new_param["width"] = getBoomerImageParamWidthForSojufile(img_param, og_clip.get("width"))
                new_param["posx"] = getBoomerImageParamPosXForSojufile(img_param)
                new_param["posy"] = getBoomerImageParamPosYForSojufile(img_param)
                new_param["triggerdelay"] = getBoomerImageParamTriggerDelayForSojufile(img_param)

                boomer_image = boomer_image + [new_param]

        if type(default.get("video")) is list :
            addvid = True

            boomer_video = []
            for vid_param in default.get("video") :
                new_param = {}

                new_param["file"] = getBoomerVideoParamFile(vid_param)
                new_param["dir"] = getBoomerVideoParamDirForSojufile(vid_param)
                new_param["mergestrategy"] = getBoomerVideoParamMergeStrategyForSojufile(vid_param)
                new_param["duration"] = getBoomerVideoParamDurationForSojufile(vid_param)
                new_param["height"] = getBoomerVideoParamHeightForSojufile(vid_param, og_clip.get("height"))
                new_param["width"] = getBoomerVideoParamWidthForSojufile(vid_param, og_clip.get("width"))
                new_param["posx"] = getBoomerVideoParamPosXForSojufile(vid_param)
                new_param["posy"] = getBoomerVideoParamPosYForSojufile(vid_param)
                new_param["triggerdelay"] = getBoomerVideoParamTriggerDelayForSojufile(vid_param)
                new_param["volume"] = getBoomerVideoParamVolumeForSojufile(vid_param)

                boomer_video = boomer_video + [new_param]


        if type(default.get("audio")) is list :
            addaud = True                        

            boomer_audio = []
            for aud_param in default.get("audio") :
                new_param = {}

                new_param["file"] = getBoomerAudioParamFile(aud_param)
                new_param["dir"] = getBoomerAudioParamDirForSojufile(aud_param)
                new_param["duration"] = getBoomerAudioParamDurationForSojufile(aud_param)
                new_param["triggerdelay"] = getBoomerAudioParamTriggerDelayForSojufile(aud_param)
                new_param["volume"] = getBoomerAudioParamVolumeForSojufile(aud_param)

                boomer_audio = boomer_audio + [new_param]

    else :
        addvid = True

        dapin = as_json_string(variables.DEFAULT_API_NAME)
        dapim = as_json_string(variables.DEFAULT_API_MODEL)

        dbt = variables.DEFAULT_BOOM_TRIGGER

        boomer_image = [
            {
                "file": variables.DEFAULT_IMAGE_FILE,
            }
        ]

        boomer_video = [
            {
                "file": variables.DEFAULT_VIDEO_FILE,
            }
        ]
        
        boomer_audio = [
            {
                "file": variables.DEFAULT_AUDIO_FILE,
            }
        ]        

    if dbt :
        boomtriggerdefault = ( 
f"""
                        "trigger": {json.dumps(dbt)}                           
                        """)
    else :
        boomtriggerdefault = ""
    
    if addimg :
        imagedefaults = ( 
f""",
                        "image": {json.dumps(boomer_image)}                           
                        """)
    else :
        imagedefaults = ""

    if addvid :
        videodefaults = ( 
f""",
                        "video": {json.dumps(boomer_video)}
                        """)
    else :
        videodefaults = ""

    if addaud :
        audiodefaults = ( 
f""",
                        "audio": {json.dumps(boomer_audio)}
                        
""")
    else :
        audiodefaults = ""


    return f""" {{
                    "generals": {{                                          
                        "api": {{
                            "name": {dapin},
                            "model": {dapim}
                        }}
                    }},

                    "defaults": {{
                        "word": {{
                            {boomtriggerdefault}
                        }}

                        {imagedefaults}

                        {videodefaults}

                        {audiodefaults}

                    }}
                }}"""






def get_boomer_generator_as_dict(generator= None) :
    aux = create_boomer_generator_as_str(generator)
    print(aux)
    return json.loads(aux)












def getFile(files= []):
    if len(files) > 0:
        return random.choice(files)
    
    else:
        return None



def buildBoomer(obj, image_file_dirs= {}, audio_file_dirs= {}, video_file_dirs= {}, default= None):

    obj["word"] = {
        "content": obj["word"],
        "start": obj["start"],
        "end": obj["end"],
    }

    bt = getBoomTriggerForSojufile(default)
    if bt :
        obj["word"]["trigger"] = bt

    if default.get("image") is not None :
        obj["image"] = []
        for param in default.get("image") :
            new_b_param = {}

            param_dir = getBoomerImageParamDirForSojufile(param)
            if param_dir is not None :
                new_b_param["dir"] = param_dir
            else :
                param_dir = getBoomerImageParamDirForFFMPEG(param)

            new_b_param["file"] = getBoomerImageParamFileForFFMPEG(param, image_file_dirs.get(param_dir))
            
            ms = getBoomerImageParamMergeStrategy(param)
            if ms is not None :
                new_b_param["mergestrategy"] = ms

            dur = getBoomerImageParamDuration(param)
            if dur is not None :
                new_b_param["duration"] = dur                                

            h = getBoomerImageParamHeight(param)
            if h is not None :
                new_b_param["height"] = h                                

            w = getBoomerImageParamWidth(param)
            if w is not None :
                new_b_param["width"] = w                                

            x = getBoomerImageParamPosX(param)
            if x is not None :
                new_b_param["posx"] = x                                

            y = getBoomerImageParamPosY(param)
            if y is not None :
                new_b_param["posy"] = y                                

            td = getBoomerImageParamTriggerDelay(param)
            if td is not None :
                new_b_param["triggerdelay"] = td                                

            obj["image"].append(new_b_param)



    if default.get("audio") is not None :
        obj["audio"] = []
        for param in default.get("audio") :
            new_b_param = {}

            param_dir = getBoomerAudioParamDirForSojufile(param)
            if param_dir is not None :
                new_b_param["dir"] = param_dir
            else :
                param_dir = getBoomerAudioParamDirForFFMPEG(param)

            new_b_param["file"] = getBoomerAudioParamFileForFFMPEG(param, audio_file_dirs.get(param_dir))
            

            dur = getBoomerAudioParamDuration(param)
            if dur is not None :
                new_b_param["duration"] = dur                                

            td = getBoomerAudioParamTriggerDelay(param)
            if td is not None :
                new_b_param["triggerdelay"] = td                                

            vol = getBoomerAudioParamVolume(param)
            if vol is not None :
                new_b_param["volume"] = vol                                

            obj["audio"].append(new_b_param)


    if default.get("video") is not None :
        obj["video"] = []
        for param in default.get("video") :
            new_b_param = {}

            param_dir = getBoomerVideoParamDirForSojufile(param)
            if param_dir is not None :
                new_b_param["dir"] = param_dir
            else :
                param_dir = getBoomerVideoParamDirForFFMPEG(param)

            new_b_param["file"] = getBoomerVideoParamFileForFFMPEG(param, video_file_dirs.get(param_dir)) 
            
            ms = getBoomerVideoParamMergeStrategy(param)
            if ms is not None :
                new_b_param["mergestrategy"] = ms

            dur = getBoomerVideoParamDuration(param)
            if dur is not None :
                new_b_param["duration"] = dur                                

            h = getBoomerVideoParamHeight(param)
            if h is not None :
                new_b_param["height"] = h                                

            w = getBoomerVideoParamWidth(param)
            if w is not None :
                new_b_param["width"] = w                                

            x = getBoomerVideoParamPosX(param)
            if x is not None :
                new_b_param["posx"] = x                                

            y = getBoomerVideoParamPosY(param)
            if y is not None :
                new_b_param["posy"] = y                                

            td = getBoomerVideoParamTriggerDelay(param)
            if td is not None :
                new_b_param["triggerdelay"] = td                                

            vol = getBoomerVideoParamVolume(param)
            if vol is not None :
                new_b_param["volume"] = vol                                

            obj["video"].append(new_b_param)
    
    if obj.get("conf") :
        del obj["conf"]
    if obj.get("end") :
        del obj["end"]
    if obj.get("start") :        
        del obj["start"]

    return obj
