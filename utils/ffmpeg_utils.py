import subprocess
import json

from .settings import variables



def get_boomers(jsonfilepath):
    describe_json = []
    with open(jsonfilepath, 'r') as f:
        describe_json = f.read()

    return json.loads(describe_json)["boomers"]












    











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
        variables.FFMPEG_PATH,
        "-y",
        "-i",
        video_file_path,
        "-filter_complex",
        """
        [0] trim= end= {0}, setpts=PTS-STARTPTS [botv]; [0] atrim= end= {0},asetpts=PTS-STARTPTS [bota];
        [0] trim= start= {0}, setpts=PTS-STARTPTS [uppv]; [0] atrim= start= {0},asetpts=PTS-STARTPTS [uppa]
        """.format(str(boomin_time)),
        "-map",
        "[botv]",
        "-map",
        "[bota]",
        *variables.FFMPEG_OUTPUT_SPECS,
        bottom_half_file,
        "-map",
        "[uppv]",
        "-map",
        "[uppa]",
        *variables.FFMPEG_OUTPUT_SPECS,
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
            variables.FFMPEG_PATH,
            "-y",
            "-ss",
            str(former_boomin_time),
            "-to",
            str(boomin_time),
            "-i",
            video_file_path,
            *variables.FFMPEG_OUTPUT_SPECS,
            "{}/{}".format(tmp_dir, current_temp_file_name)
        ])

        former_boomin_time = boomin_time
        
    current_temp_file_name = "clip_piece_{}.mp4".format(len(boomers))
    
    subprocess.run([
        variables.FFMPEG_PATH,
        "-y",
        "-ss",
        str(former_boomin_time),
        "-i",
        video_file_path,
        *variables.FFMPEG_OUTPUT_SPECS,
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
            variables.FFMPEG_PATH,
            "-y",
            "-i",
            boomer_audio,
            "-i",
            "{}/{}".format(tmp_dir, current_temp_file_name),
            "-filter_complex",
            "[0] [1] amix",
            *variables.FFMPEG_OUTPUT_SPECS,
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
        *variables.FFMPEG_OUTPUT_SPECS,        
        "output_video.mp4"
    ])

def concatClipHalves(output_file, tmp_dir):

    subprocess.run([
        "ffmpeg",
        "-y",
        "-r",
        variables.FFMPEG_FPS,
        "-i",
        tmp_dir + "/" + "bottom_half.mp4",
        "-r",
        variables.FFMPEG_FPS,
        "-i",
        tmp_dir + "/" + "upper_half.mp4",        
        "-filter_complex",
        "[0:v] [0:a] [1:v] [1:a] concat=n=2:v=1:a=1 [outv] [outa]",
        "-map",
        "[outv]",
        "-map",
        "[outa]",
        *variables.FFMPEG_OUTPUT_SPECS,
        output_file
    ])

def quickOverlay(videofilepath= "", boomer= None, output_file= "overlay.mp4", tmp_dir= "."):
    if boomer["image"]["file"] == None:
        return
    
    media = variables.DEFAULT_IMAGE_PATH + boomer["image"]["file"]
    bommin_time_start = boomer["word"][boomer["image"]["conf"]["boom_trigger"]]
    boomin_time_end = bommin_time_start + boomer["image"]["conf"]["max_duration"]

    subprocess.run([
        variables.FFMPEG_PATH,
        "-y",
        "-i",
        videofilepath,
        "-i",
        media,        
        "-filter_complex",
        "overlay= enable='between(t,{:.2f},{:.2f})'".format(bommin_time_start, boomin_time_end),
        *variables.FFMPEG_OUTPUT_SPECS,
        tmp_dir + "/" + output_file
    ])

def amixUpperHalfVideo(boomer= None, tmp_dir= "."):
    if boomer["audio"]["files"] == None:
        return
    
    upper_half_file_tmp = "{}/upper_half_0.mp4".format(tmp_dir)
    upper_half_file_final = "{}/upper_half.mp4".format(tmp_dir)

    media = variables.DEFAULT_AUDIO_PATH + boomer["audio"]["files"][0]

    subprocess.run([
        variables.FFMPEG_PATH,
        "-y",
        "-i",
        upper_half_file_tmp,
        "-i",
        media,        
        "-filter_complex",
        "[1] [0] amix",
        *variables.FFMPEG_OUTPUT_SPECS,
        upper_half_file_final
    ])












def quickAmix(videofilepath= "", boomer= [], output_file= "amix.mp4", tmp_dir= "."):
    if boomer["audio"]["files"] == None:
        return
    
    media = variables.DEFAULT_AUDIO_PATH + boomer["audio"]["files"][0]
    bommin_time_start = boomer["word"][boomer["image"]["conf"]["boom_trigger"]]

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i",
        videofilepath,
        "-async",
        "1",
        "-itsoffset",
        str(bommin_time_start),
        "-i",
        media,
        "-filter_complex",
        "[0:a]volume=1[a0]; [1:a]volume=1[a1]; [a1] [a0] amix=inputs=2:normalize=0",
        *variables.FFMPEG_OUTPUT_SPECS,
        tmp_dir + "/" + output_file
    ])    


def slowAmix(videofilepath= "", boomer= [], output_file= "amix.mp4", tmp_dir= "."):
    if boomer["audio"]["files"] == None:
        return
    
    media = variables.DEFAULT_AUDIO_PATH + boomer["audio"]["files"][0]
    bommin_time_start = boomer["word"][boomer["image"]["conf"]["boom_trigger"]]

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i",
        videofilepath,
        "-async",
        "1",
        "-itsoffset",
        str(bommin_time_start),
        "-i",
        media,
        "-filter_complex",
        "[0:a]volume=1[a0]; [1:a]volume=1[a1]; [a1] [a0] amix=inputs=2:normalize=0",
        *variables.FFMPEG_OUTPUT_SPECS,
        tmp_dir + "/" + output_file
    ])













def copy(from_= "", to_= ""):
    
    subprocess.run([
        variables.FFMPEG_PATH,
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