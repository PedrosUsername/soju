import subprocess
import json

from .settings import variables



def get_boomers(jsonfilepath):
    describe_json = []
    with open(jsonfilepath, 'r') as f:
        describe_json = f.read()

    return json.loads(describe_json)["boomers"]



ffmpeg = "/usr/local/bin/ffmpeg"
fps = "30"




def splitClip(videofilepath= None, boomers= [], tmp_dir= ""):
    ffmpegSplitClipByBoomers(videofilepath, boomers, tmp_dir)







    











def get_boom_trigger(boomer= None):
    if boomer is None:
        return variables.DEFAULT_BOOM_TRIGGER if variables.DEFAULT_BOOM_TRIGGER is not None else "end"
    else:
        return boomer["image"]["conf"]["boom_trigger"]
    

    
def ffmpegSplitClipByBoomers(video_file_path="", boomers= [], tmp_dir= ""):

    former_boomin_time = 0
    for counter, boomer in enumerate(boomers):
        boomin_time = boomer["word"][get_boom_trigger(boomer)]
        current_temp_file_name = "clip_piece_{}.mp4".format(counter)
        current_temp_audio_file_name = "ready_clip_piece_{}.wav".format(counter)

        if counter == 0:
            current_temp_file_name = "ready_" + current_temp_file_name

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
                "{}/{}".format(tmp_dir, current_temp_audio_file_name)
            ])
        
        subprocess.run([
            ffmpeg,
            "-y",
            "-ss",
            str(former_boomin_time),
            "-to",
            str(boomin_time),
            "-i",
            video_file_path,
            "-c",
            "copy",
            "-r",
            fps,
            "{}/{}".format(tmp_dir, current_temp_file_name)
        ])

        former_boomin_time = boomin_time
        
    current_temp_file_name = "clip_piece_{}.mp4".format(len(boomers))
    
    subprocess.run([
        ffmpeg,
        "-y",
        "-ss",
        str(former_boomin_time),
        "-i",
        video_file_path,
        "-c",
        "copy",
        "-r",
        fps,        
        "{}/{}".format(tmp_dir, current_temp_file_name)
    ])



def buildAudio(boomers= None, tmp_dir= ""):
    for counter, boomer in enumerate(boomers, 1):
        if boomer["audio"] is None or boomer["audio"]["files"] is None:
            continue

        boomer_audio = '{0}{1}'.format(variables.DEFAULT_AUDIO_PATH, boomer["audio"]["files"][0] if boomer["audio"]["files"][0] is not None else variables.DEFAULT_NULL_AUDIO_FILE)
        current_temp_file_name = "ready_clip_piece_{}.mp4".format(counter)
        output_temp_file_name = "ready_clip_piece_{}.wav".format(counter)

        subprocess.run([
            ffmpeg,
            "-y",
            "-i",
            "{}/{}".format(tmp_dir, current_temp_file_name),
            "-i",
            boomer_audio,
            "-filter_complex",
            "[0:a] [1:a] amix ",
            "{}/{}".format(tmp_dir, output_temp_file_name)
        ])            



def concatAudioClips(tmp_dir):
    subprocess.run([
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        tmp_dir + "/" + "params.txt",
        "-c",
        "copy",
        "output_audio.wav"
    ])

def concatVideoClips(tmp_dir):
    subprocess.run([
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        tmp_dir + "/" + "params.txt",
        "-c",
        "copy",
        "output_video.mp4"
    ])

def mixAudioAndVideo(tmp_dir):
    subprocess.run([
        "ffmpeg",
        "-y",
        "-i",
        "output_video.mp4",
        "-i",
        "output_audio.wav",
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "final.mp4"
    ])


# merge video w audio
# ffmpeg -i ./assets/video/vox.mp4 -i ./assets/audio/vineboom.mp3 -filter_complex '[0:a][1:a] amix [y]' -c:v copy -c:a aac -map 0:v -map [y]:a output.mp4

# merge image w audio
# ffmpeg -r 1 -loop 1 -i ./assets/image/cursed/aaa.jpeg -i ./assets/audio/vineboom.mp3 -c:a copy -r 1 -vcodec libx264 -shortest output.mp4
# https://superuser.com/questions/1041816/combine-one-image-one-audio-file-to-make-one-video-using-ffmpeg?answertab=createdasc#tab-top