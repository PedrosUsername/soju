import random
import os
import ntpath


from .settings import variables



HISTORY_LIMIT = 200



def get_base_file_name_from(videofilepath= None) :
    if videofilepath is None :
        return None
    
    filename = ntpath.basename(videofilepath)
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


