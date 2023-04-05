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




def splitClip(videofilepath= None, jsonfilepath= None, tmp_dir= "", clip_duration= 0):
    boomers = get_boomers(jsonfilepath)
    ffmpegSplitClipByBoomers(videofilepath, boomers, tmp_dir, clip_duration)







    











def get_boom_trigger(boomer= None):
    if boomer is None:
        return variables.DEFAULT_BOOM_TRIGGER if variables.DEFAULT_BOOM_TRIGGER is not None else "end"
    else:
        return boomer["image"]["conf"]["boom_trigger"]
    

    
def ffmpegSplitClipByBoomers(video_file_path="", boomers= [], tmp_dir= "", clip_duration= 0):
    out_of_range_boomer_count = 0
   
    former_boomin_time = 0
    for counter, boomer in enumerate(boomers):
        actual_counter = counter - out_of_range_boomer_count

        boomin_time = boomer["word"][get_boom_trigger(boomer)]
        current_temp_file_name = "clip_piece_{}.mp4".format(actual_counter)

        if boomin_time > 0 and boomin_time < clip_duration:
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
                tmp_dir + current_temp_file_name
            ])

            former_boomin_time = boomin_time
        else:
            out_of_range_boomer_count += 1
        
    
    current_temp_file_name = "clip_piece_{}.mp4".format(len(boomers) - out_of_range_boomer_count)
    
    subprocess.run([
        ffmpeg,
        "-y",
        "-ss",
        str(former_boomin_time),
        "-i",
        video_file_path,
        "-r",
        fps,        
        tmp_dir + current_temp_file_name
    ])
    
# merge video w audio
# ffmpeg -i ./assets/video/vox.mp4 -i ./assets/audio/vineboom.mp3 -filter_complex '[0:a][1:a] amix [y]' -c:v copy -c:a aac -map 0:v -map [y]:a output.mp4

# merge image w audio
# ffmpeg -r 1 -loop 1 -i ./assets/image/cursed/aaa.jpeg -i ./assets/audio/vineboom.mp3 -c:a copy -r 1 -vcodec libx264 -shortest output.mp4
# https://superuser.com/questions/1041816/combine-one-image-one-audio-file-to-make-one-video-using-ffmpeg?answertab=createdasc#tab-top