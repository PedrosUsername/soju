import ntpath

from moviepy.editor import *







og_clip_params = {}


def get_og_clip_params() :
    global og_clip_params
    return og_clip_params



def set_og_clip_params(params) :
    global og_clip_params
    og_clip_params = params


def init_og_clip_params(clip_path= None) :

    clip = VideoFileClip( clip_path )

    if clip.duration > 300 :
        raise Exception("media duration exceeds the current limit")

    og_clip_params = {
        "file": clip_path,
        "duration": clip.duration,
        "width": clip.size[0],
        "height": clip.size[1]
    }

    set_og_clip_params(og_clip_params)





















def get_base_file_name_from(videofilepath= None):
    if videofilepath is None :
        return None
    
    filename = ntpath.basename(videofilepath)
    head, tail = filename[::-1].split(".", 1)
    return tail[::-1]



def generate_soju_file_name(videofilepath):
    videofilename = get_base_file_name_from(videofilepath)
    return "{}.soju.json".format(videofilename)



def generate_output_file_name(videofilepath):
    videofilename = get_base_file_name_from(videofilepath)
    return "{}.mp4".format(videofilename)
