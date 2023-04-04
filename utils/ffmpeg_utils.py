import subprocess
import json

from .settings import variables



def get_boomers(jsonfilepath):
    describe_json = []
    with open(jsonfilepath, 'r') as f:
        describe_json = f.read()

    return json.loads(describe_json)["boomers"]



ffmpeg = "/usr/bin/ffmpeg"
fps = "30"




def soju(videofilepath= None, jsonfilepath= None):
    boomers = get_boomers(jsonfilepath)
    clip_pieces = ffmpegSplitClipByBoomers(videofilepath, boomers)

    
    print(clip_pieces)








    











def get_boom_trigger(boomer= None):
    if boomer is None:
        return variables.DEFAULT_BOOM_TRIGGER if variables.DEFAULT_BOOM_TRIGGER is not None else "end"
    else:
        return boomer["image"]["conf"]["boom_trigger"]
    

    
def ffmpegSplitClipByBoomers(video_file_path="", boomers= []):
    pieces = []
   
    former_boomin_time = 0
    for counter, boomer in enumerate(boomers):
        boomin_time = boomer["word"][get_boom_trigger(boomer)]
        current_temp_file_name = "clip_piece_{}.mp4".format(counter)
        pieces = pieces + [current_temp_file_name]

        subprocess.run([
            ffmpeg,
            "-y",
            "-ss",
            str(former_boomin_time),
            "-to",
            str(boomin_time),
            "-i",
            video_file_path,
            "-r",
            fps,
            "./utils/tmp_files/{}".format(current_temp_file_name)
        ])

        former_boomin_time = boomin_time
    
    current_temp_file_name = "clip_piece_{}.mp4".format(len(boomers))
    pieces = pieces + [current_temp_file_name]
    
    subprocess.run([
        ffmpeg,
        "-y",
        "-ss",
        str(former_boomin_time),
        "-i",
        video_file_path,
        "-r",
        fps,        
        "./utils/tmp_files/{}".format(current_temp_file_name)
    ])
    
    return pieces
    
# merge video w audio
# ffmpeg -i ./assets/video/vox.mp4 -i ./assets/audio/vineboom.mp3 -filter_complex '[0:a][1:a] amix [y]' -c:v copy -c:a aac -map 0:v -map [y]:a output.mp4

# merge image w audio
# ffmpeg -r 1 -loop 1 -i ./assets/image/cursed/aaa.jpeg -i ./assets/audio/vineboom.mp3 -c:a copy -r 1 -vcodec libx264 -shortest output.mp4
# https://superuser.com/questions/1041816/combine-one-image-one-audio-file-to-make-one-video-using-ffmpeg?answertab=createdasc#tab-top