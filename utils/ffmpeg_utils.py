import subprocess
import json

from .settings import variables



def get_boomers(jsonfilepath):
    describe_json = []
    with open(jsonfilepath, 'r') as f:
        describe_json = f.read()

    return json.loads(describe_json)["boomers"]



ffmpeg = "/snap/bin/ffmpeg"
fps = "30"
video_codec = "h264"
audio_codec = "mp3"
video_bitrate = "64k"
audio_bitrate = "196k"
sample_rate = "44100"
encoding_speed = "fast"
crf = "22"
frame_size = "1280x720"
pix_fmt = "yuv420p"
bufsize = "64k"









    











def get_boom_trigger(boomer= None):
    if boomer is None:
        return variables.DEFAULT_BOOM_TRIGGER if variables.DEFAULT_BOOM_TRIGGER is not None else "end"
    else:
        return boomer["image"]["conf"]["boom_trigger"]
    


def splitClip(video_file_path="", boomer= [], tmp_dir= "."):
    boomin_time = boomer["word"][get_boom_trigger(boomer)]

    bottom_half_file = "{}/bottom_half.mp4".format(tmp_dir)
    upper_half_file = "{}/upper_half_0.mp4".format(tmp_dir)
    
    subprocess.run([
        ffmpeg,
        "-y",
        "-i",
        video_file_path,
        "-filter_complex",
        "trim= end= " + str(boomin_time) + ", setpts=PTS-STARTPTS [botv]; atrim= end= " + str(boomin_time) + ",asetpts=PTS-STARTPTS [bota]",
        "-map",
        "[botv]",
        "-map",
        "[bota]",
        "-c:v",
        video_codec,
        "-c:a",
        audio_codec,
        "-b:v",
        video_bitrate,
        "-b:a",
        audio_bitrate,
        "-preset",
        encoding_speed,
        "-crf",
        crf,
        "-s",
        frame_size,
        "-ar",
        sample_rate,
        "-pix_fmt",
        pix_fmt,
        "-video_track_timescale",
        "90000",
        "-r",
        fps,
        bottom_half_file
    ])

    subprocess.run([
        ffmpeg,
        "-y",
        "-i",
        video_file_path,
        "-filter_complex",
        "trim= start= " + str(boomin_time) + ", setpts=PTS-STARTPTS [uppv]; atrim= start= " + str(boomin_time) + ",asetpts=PTS-STARTPTS [uppa]",
        "-map",
        "[uppv]",
        "-map",
        "[uppa]",
        "-c:v",
        video_codec,
        "-c:a",
        audio_codec,
        "-b:v",
        video_bitrate,
        "-b:a",
        audio_bitrate,
        "-preset",
        encoding_speed,
        "-crf",
        crf,
        "-s",
        frame_size,
        "-ar",
        sample_rate,
        "-pix_fmt",
        pix_fmt,
        "-video_track_timescale",
        "90000",
        "-r",
        fps,
        upper_half_file
    ])
    
    

def splitClipByBoomers(video_file_path="", boomers= [], tmp_dir= "."):
    former_boomin_time = 0
    for counter, boomer in enumerate(boomers):
        boomin_time = boomer["word"][get_boom_trigger(boomer)]
        current_temp_file_name = "clip_piece_{}.mp4".format(counter)

        if counter == 0:
            current_temp_file_name = "ready_clip_piece_0.mp4"
        
        subprocess.run([
            ffmpeg,
            "-y",
            "-ss",
            str(former_boomin_time),
            "-to",
            str(boomin_time),
            "-i",
            video_file_path,
            "-c:v",
            video_codec,
            "-c:a",
            audio_codec,
            "-b:v",
            video_bitrate,
            "-b:a",
            audio_bitrate,
            "-preset",
            encoding_speed,
            "-crf",
            crf,
            "-s",
            frame_size,
            "-ar",
            sample_rate,
            "-pix_fmt",
            pix_fmt,
            "-video_track_timescale",
            "90000",
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
        "-c:v",
        video_codec,
        "-c:a",
        audio_codec,
        "-b:v",
        video_bitrate,
        "-b:a",
        audio_bitrate,
        "-preset",
        encoding_speed,
        "-crf",
        crf,
        "-s",
        frame_size,
        "-ar",
        sample_rate,
        "-pix_fmt",
        pix_fmt,
        "-video_track_timescale",
        "90000",
        "-r",
        fps,
        "{}/{}".format(tmp_dir, current_temp_file_name)
    ])



def buildAudio(boomers= None, tmp_dir= "."):
    for counter, boomer in enumerate(boomers, 1):
        if boomer["audio"] is None or boomer["audio"]["files"] is None or len(boomer["audio"]["files"]) < 1:
            boomer_audio = variables.DEFAULT_NULL_AUDIO_FILE
        else:
            boomer_audio = '{0}{1}'.format(variables.DEFAULT_AUDIO_PATH, boomer["audio"]["files"][0] if boomer["audio"]["files"][0] is not None else variables.DEFAULT_NULL_AUDIO_FILE)
            
        current_temp_file_name = "v_clip_piece_{}.mp4".format(counter)
        output_temp_file_name = "ready_clip_piece_{}.mp4".format(counter)

        subprocess.run([
            ffmpeg,
            "-y",
            "-i",
            boomer_audio,
            "-i",
            "{}/{}".format(tmp_dir, current_temp_file_name),
            "-filter_complex",
            "[0] [1] amix",
            "-c:v",
            video_codec,
            "-c:a",
            audio_codec,
            "-b:v",
            video_bitrate,
            "-b:a",
            audio_bitrate,
            "-preset",
            encoding_speed,
            "-crf",
            crf,
            "-s",
            frame_size,
            "-ar",
            sample_rate,
            "-pix_fmt",
            pix_fmt,
            "-video_track_timescale",
            "90000",
            "-r",
            fps,
            "{}/{}".format(tmp_dir, output_temp_file_name)
        ])



def concatClips(concat_file, tmp_dir):
    subprocess.run([
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        tmp_dir + "/" + concat_file,
        "-c:v",
        video_codec,
        "-c:a",
        audio_codec,
        "-b:v",
        video_bitrate,
        "-b:a",
        audio_bitrate,
        "-preset",
        encoding_speed,
        "-crf",
        crf,
        "-s",
        frame_size,
        "-ar",
        sample_rate,
        "-pix_fmt",
        pix_fmt,
        "-video_track_timescale",
        "90000",
        "-r",
        fps,        
        "output_video.mp4"
    ])

def concatClipHalves(output_file, tmp_dir):

    subprocess.run([
        "ffmpeg",
        "-y",
        "-r",
        fps,
        "-i",
        tmp_dir + "/" + "bottom_half.mp4",
        "-r",
        fps,
        "-i",
        tmp_dir + "/" + "upper_half.mp4",        
        "-filter_complex",
        "[0:v] [0:a] [1:v] [1:a] concat=n=2:v=1:a=1 [outv] [outa]",
        "-map",
        "[outv]",
        "-map",
        "[outa]",
        "-c:v",
        video_codec,
        "-c:a",
        audio_codec,
        "-b:v",
        video_bitrate,
        "-b:a",
        audio_bitrate,
        "-preset",
        encoding_speed,
        "-crf",
        crf,
        "-s",
        frame_size,
        "-ar",
        sample_rate,
        "-pix_fmt",
        pix_fmt,
        "-video_track_timescale",
        "90000",
        "-r",
        fps,
        output_file
    ])

def quickOverlay(videofilepath= "", boomer= None, output_file= "overlay.mp4", tmp_dir= "."):
    if boomer["image"]["file"] == None:
        return
    
    media = variables.DEFAULT_IMAGE_PATH + boomer["image"]["file"]
    bommin_time_start = boomer["word"][boomer["image"]["conf"]["boom_trigger"]]
    boomin_time_end = bommin_time_start + boomer["image"]["conf"]["max_duration"]

    subprocess.run([
        ffmpeg,
        "-y",
        "-i",
        videofilepath,
        "-i",
        media,        
        "-filter_complex",
        "overlay= enable='between(t,{:.2f},{:.2f})'".format(bommin_time_start, boomin_time_end),
        "-c:v",
        video_codec,
        "-c:a",
        audio_codec,
        "-b:v",
        video_bitrate,
        "-b:a",
        audio_bitrate,
        "-preset",
        encoding_speed,
        "-crf",
        crf,
        "-s",
        frame_size,
        "-ar",
        sample_rate,
        "-pix_fmt",
        pix_fmt,
        "-video_track_timescale",
        "90000",
        "-r",
        fps,
        tmp_dir + "/" + output_file
    ])


def copy(from_= "", to_= ""):
    
    subprocess.run([
        ffmpeg,
        "-y",
        "-i",
        from_,
        '-c',
        "copy",
        to_
    ])
# merge video w audio
# ffmpeg -i ./assets/video/vox.mp4 -i ./assets/audio/vineboom.mp3 -filter_complex '[0:a][1:a] amix [y]' -c:v copy -c:a aac -map 0:v -map [y]:a output.mp4

# merge image w audio
# ffmpeg -r 1 -loop 1 -i ./assets/image/cursed/aaa.jpeg -i ./assets/audio/vineboom.mp3 -c:a copy -r 1 -vcodec libx264 -shortest output.mp4
# https://superuser.com/questions/1041816/combine-one-image-one-audio-file-to-make-one-video-using-ffmpeg?answertab=createdasc#tab-top

"""
ffmpeg -y -r 30 -i ready_clip_piece_0.mp4 -r 30 -i ready_clip_piece_1.mp4 -r 30 -i ready_clip_piece_2.mp4 -r 30 -i ready_clip_piece_3.mp4 -r 30 -i ready_clip_piece_4.mp4 -filter_complex "[0:v] [0:a] [1:v] [1:a] [2:v] [2:a] [3:v] [3:a] [4:v] [4:a] concat=n=5:v=1:a=1 [outv] [outa]" -map "[outv]" -map "[outa]" -r 30 -c:v h264 -c:a mp3 -b:v 64k -b:a 196k -ar 44100 -preset fast -crf 22 -s 1280x720 -pix_fmt yuv420p -video_track_timescale 90000 outpooooot.mp4
"""