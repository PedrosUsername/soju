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
