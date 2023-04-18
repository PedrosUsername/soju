import subprocess
import json

from .settings import variables



FFMPEG_PATH = variables.FFMPEG_PATH
FFMPEG_OUTPUT_SPECS = variables.FFMPEG_OUTPUT_SPECS
IMAGE_FOLDER = variables.DEFAULT_IMAGE_FOLDER
AUDIO_FOLDER = variables.DEFAULT_AUDIO_FOLDER













def get_boomers(jsonfilepath):
    describe_json = []
    with open(jsonfilepath, 'r') as f:
        describe_json = f.read()

    return json.loads(describe_json)["boomers"]












    









def getBoomerImageWidth(boomer= None):
    if not boomer or not boomer["image"] or not boomer["image"]["conf"] or not boomer["image"]["conf"]["width"]:
        return 0
    else:
        return boomer["image"]["conf"]["width"]
    
def getBoomerImageHeight(boomer= None):
    if not boomer or not boomer["image"] or not boomer["image"]["conf"] or not boomer["image"]["conf"]["height"]:
        return 0
    else:
        return boomer["image"]["conf"]["height"]    

def get_boom_trigger(boomer= None):
    if not boomer or not boomer["word"] or not boomer["word"]["trigger"]:
        return variables.DEFAULT_BOOM_TRIGGER if variables.DEFAULT_BOOM_TRIGGER is not None else "end"
    else:
        return boomer["word"]["trigger"]
    

def getBoomerBoominTime(boomer= None):
    if not boomer or not boomer["word"] or not boomer["word"][get_boom_trigger()]:
        return 0
    else:
        return boomer["word"][get_boom_trigger(boomer)]
    

def getBoomerImageDuration(boomer= None):
    if not boomer or not boomer["image"] or not boomer["image"]["conf"] or not boomer["image"]["conf"]["max_duration"]:
        return 0
    else:
        return boomer["image"]["conf"]["max_duration"]
    


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
    
    media = variables.DEFAULT_IMAGE_FOLDER + boomer["image"]["file"]
    bommin_time_start = boomer["word"][boomer["word"]["trigger"]]
    boomin_time_end = bommin_time_start + boomer["image"]["conf"]["max_duration"]

    subprocess.run([
        variables.FFMPEG_PATH,
        "-y",
        "-i",
        videofilepath,
        "-i",
        media,        
        "-filter_complex",
        "overlay= x=main_w/2-overlay_w/2:y=main_h/2-overlay_h/2:enable='between(t,{:.2f},{:.2f})'".format(bommin_time_start, boomin_time_end),
        *variables.FFMPEG_OUTPUT_SPECS,
        tmp_dir + "/" + output_file
    ])





def amixUpperHalf(boomer= None, tmp_dir= "."):
    if boomer["audio"]["file"] == None:
        return
    
    upper_half_file_tmp = "{}/upper_half_0.mp4".format(tmp_dir)
    upper_half_file_final = "{}/upper_half.mp4".format(tmp_dir)

    media = variables.DEFAULT_AUDIO_FOLDER + boomer["audio"]["file"]

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















def slowAmix(videofilepath= "", boomer= [], output_file= "amix.mp4"):
    if boomer["audio"] is None or boomer["audio"]["file"] is None:
        return
    
    media = variables.DEFAULT_AUDIO_FOLDER + boomer["audio"]["file"]
    boomin_time = boomer["word"][get_boom_trigger(boomer)]

    subprocess.run([
        variables.FFMPEG_PATH,
        "-y",
        "-i",
        videofilepath,
        "-i",
        media,
        "-filter_complex",
        """
        [0] trim= end= {0}, setpts=PTS-STARTPTS [botv]; [0] atrim= end= {0},asetpts=PTS-STARTPTS [bota];
        [0] trim= start= {0}, setpts=PTS-STARTPTS [uppv]; [0] atrim= start= {0},asetpts=PTS-STARTPTS [uppa];
        
        [uppa] [1] amix=dropout_transition=0,dynaudnorm [uppar];
        
        [botv] [bota] [uppv] [uppar] concat=n=2:v=1:a=1 [outv] [outa]
        """.format(str(boomin_time)),
        "-map",
        "[outv]",
        "-map",
        "[outa]",
        *variables.FFMPEG_OUTPUT_SPECS,
        output_file
    ])





def executeFfmpegCall(params= []):
    subprocess.run(
        params
    )


def cleanFilterParams(params= "", filth= ""):
    return params[:(len(filth) * -1)]


def buildCall(videofilepath, outputfilepath= "output.mp4", boomers= None):
    image_file_boomers = [ b for b in boomers if b["image"] != None and b["image"]["file"] != None ]
    audio_file_boomers = [ b for b in boomers if b["audio"] != None and b["audio"]["file"] != None ]
    media_inputs = buildMediaInputs(image_file_boomers, audio_file_boomers)

    filter_params = "[0] scale= w= 0:h= 0 [clip]; "
    stream_mapping = []

    separator = ""
    fout_label = ""

    if len(image_file_boomers) > 0:
        main_label = "[clip]"
        separator = "; "
        fout_label = "[outv]"

        filter_params = (
            filter_params + buildImageOverlayFilterParams(image_file_boomers, inp= main_label, out= fout_label, first_file_idx= 1)
            + fout_label
            + separator
        )

    stream_mapping = stream_mapping + ["-map", fout_label]


    if len(audio_file_boomers) > 0:
        main_label = "[0]"
        separator = "; "
        fout_label = "[outa]"

        filter_params = (
            filter_params
            + buildAudioAmixFilterParams(audio_file_boomers, inp= main_label, out= fout_label, first_file_idx= len(image_file_boomers) + 1)
            + fout_label
            + separator
        )

        stream_mapping = stream_mapping + ["-map", fout_label]
    

    ffmpeg = FFMPEG_PATH
    output_specs = FFMPEG_OUTPUT_SPECS
    filter_params = cleanFilterParams(filter_params, filth= separator)

    return [
        ffmpeg,
        "-y",
        "-i",
        videofilepath,
        *media_inputs,
        "-filter_complex",
        filter_params,
        *stream_mapping,
        *output_specs,
        outputfilepath
    ]








def buildMediaInputs(image_file_boomers= [], audio_file_boomers= []):
    media_inputs = []
    
    for file in image_file_boomers:
        media_inputs = media_inputs + ["-i"] + [IMAGE_FOLDER + file["image"]["file"]]

    for file in audio_file_boomers:
        media_inputs = media_inputs + ["-i"] + [AUDIO_FOLDER + file["audio"]["file"]]

    return media_inputs







def buildImageOverlayFilterParams(boomers= [], inp= "[0]", out= "[outv]", first_file_idx= 0):
    filter_params = ""

    head = boomers[:1]
    for boomer in head:
        img_width = getBoomerImageWidth(boomer)
        img_height = getBoomerImageHeight(boomer)        
        boomin_time_start = getBoomerBoominTime(boomer)
        boomin_time_end = boomin_time_start + getBoomerImageDuration(boomer)
        filter_params = filter_params + """
[{1}] scale= w= {4}:h= {5} [img];
{0}[img] overlay= x=main_w/2-overlay_w/2:y=main_h/2-overlay_h/2:enable='between(t, {2}, {3})'
""".format(
            inp,
            first_file_idx,
            boomin_time_start,
            boomin_time_end,
            img_width,
            img_height
        )

    tail = boomers[1:]
    for idx, boomer in enumerate(tail, first_file_idx + 1):
        img_width = getBoomerImageWidth(boomer)
        img_height = getBoomerImageHeight(boomer)        
        boomin_time_start = getBoomerBoominTime(boomer)
        boomin_time_end = boomin_time_start + getBoomerImageDuration(boomer)
        filter_params = filter_params + """{0};
[{1}] scale= w= {4}:h= {5} [img];
{0}[img] overlay= x=main_w/2-overlay_w/2:y=main_h/2-overlay_h/2:enable='between(t, {2}, {3})'
""".format(
            out,
            idx,
            boomin_time_start,
            boomin_time_end,
            img_width,
            img_height
        )

    return filter_params











def buildAudioAmixFilterParams(boomers= [], inp= "[0]", out= "[outa]", first_file_idx= 0):
    filter_params = ""

    head = boomers[:1]
    for boomer in head:
        boomin_time_start = getBoomerBoominTime(boomer)
        # boomin_time_end = boomin_time_start + getBoomerImageDuration(boomer)
        filter_params = filter_params + """
{0} asplit=2\n[fin2] [fin4];
[fin2] atrim= end= {2}, asetpts=PTS-STARTPTS\n[bota];
[fin4] atrim= start= {2},asetpts=PTS-STARTPTS\n[uppa];

[uppa] [{1}] amix= dropout_transition=0, dynaudnorm\n[uppa_mix];

[bota] [uppa_mix] concat=n=2:v=0:a=1
""".format(
            inp,
            first_file_idx,
            boomin_time_start
        )

    tail = boomers[1:]
    for idx, boomer in enumerate(tail, first_file_idx + 1):
        boomin_time_start = getBoomerBoominTime(boomer)
        # boomin_time_end = boomin_time_start + getBoomerImageDuration(boomer)
        filter_params = filter_params + """{2};
{2} asplit=2\n[outa1] [outa2];
[outa1] atrim= end= {0}, asetpts=PTS-STARTPTS\n[bota];
[outa2] atrim= start= {0},asetpts=PTS-STARTPTS\n[uppa];

[uppa] [{1}] amix= dropout_transition=0, dynaudnorm\n[uppa_mix];

[bota] [uppa_mix] concat=n=2:v=0:a=1
""".format(boomin_time_start, idx, out)        
        
    return filter_params






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

1 image 0 audio:
    -filter_complex
    [0][1] overlay= x=main_w/2-overlay_w/2:y=main_h/2-overlay_h/2:enable='between(t, 1.32029, 1.92029)'

1 image 1 audio:
    -filter_complex
    [0][1] overlay= x=main_w/2-overlay_w/2:y=main_h/2-overlay_h/2:enable='between(t, 1.32029, 1.92029)';

    [0] trim= end= 1.32029, setpts=PTS-STARTPTS [botv]; [0] atrim= end= 1.32029, asetpts=PTS-STARTPTS [bota];
    [0] trim= start= 1.32029, setpts=PTS-STARTPTS [uppv]; [0] atrim= start= 1.32029,asetpts=PTS-STARTPTS [uppa];
    [uppa] [2] amix= dropout_transition=0, dynaudnorm [uppa_mix];
    [botv] [bota] [uppv] [uppa_mix] concat=n=2:v=1:a=1 [outv] [outa]

0 image 1 audio:
    -filter_complex
    [0] trim= end= 1.32029, setpts=PTS-STARTPTS [botv]; [0] atrim= end= 1.32029, asetpts=PTS-STARTPTS [bota];
    [0] trim= start= 1.32029, setpts=PTS-STARTPTS [uppv]; [0] atrim= start= 1.32029,asetpts=PTS-STARTPTS [uppa];
    [uppa] [1] amix= dropout_transition=0, dynaudnorm [uppa_mix];
    [botv] [bota] [uppv] [uppa_mix] concat=n=2:v=1:a=1 [outv] [outa]

2 image 0 audio:
    -filter_complex
    [0][1] overlay= x=main_w/2-overlay_w/2:y=main_h/2-overlay_h/2:enable='between(t, 1.32029, 1.92029)' [overlaid];

    [overlaid][2] overlay= x=main_w/2-overlay_w/2:y=main_h/2-overlay_h/2:enable='between(t, 4.83, 5.43)'

0 image 2 audio:
    [0] trim= end= 1.32029, setpts=PTS-STARTPTS [botv]; [0] atrim= end= 1.32029, asetpts=PTS-STARTPTS [bota];
    [0] trim= start= 1.32029, setpts=PTS-STARTPTS [uppv]; [0] atrim= start= 1.32029,asetpts=PTS-STARTPTS [uppa];
    [uppa] [1] amix= dropout_transition=0, dynaudnorm [uppa_mix];
    [botv] [bota] [uppv] [uppa_mix] concat=n=2:v=1:a=1 [outv] [outa];

    [outa] asplit=2 [outa1] [outa2];
    [outa1] atrim= end= 4.83, asetpts=PTS-STARTPTS [bota];
    [outa2] atrim= start= 4.83,asetpts=PTS-STARTPTS [uppa];

    [uppa] [2] amix= dropout_transition=0, dynaudnorm [uppa_mix];

    [bota] [uppa_mix] concat=n=2:v=0:a=1 [outa]    
"""




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
        if boomer["audio"] is None or boomer["audio"]["file"] is None or len(boomer["audio"]["file"]) < 1:
            boomer_audio = variables.DEFAULT_NULL_AUDIO_FILE
        else:
            boomer_audio = '{0}{1}'.format(variables.DEFAULT_AUDIO_FOLDER, boomer["audio"]["file"] if boomer["audio"]["file"] is not None else variables.DEFAULT_NULL_AUDIO_FILE)
            
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

def quickAmix(videofilepath= "", boomer= [], output_file= "amix.mp4", tmp_dir= "."):
    if boomer["audio"]["file"] == None:
        return
    
    media = variables.DEFAULT_AUDIO_FOLDER + boomer["audio"]["file"]
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



"""

--------------------- video overlay ---

ffmpeg
-i clip.mp4

-i image_1.png
-i image_2.png
[...]
-i image_n.png

-filter_complex
    [0][1] overlay= enable='between(t, bt1, bt1+duration)'
    [out_1]; [out_1][2] overlay= enable='between(t, bt2, bt2+duration)'
    [...]
    [out_n-1]; [out_n-1][n] overlay= enable='between(t, btn, btn+duration)'

*variables.FFMPEG_OUTPUT_SPECS,

output_file.mp4




----------------------- audio overlay ---

ffmpeg
-i clip.mp4

-i audio_1.png
-i audio_2.png
[...]
-i audio_n.png

-filter_complex
    [0] trim= end= bt1, setpts=PTS-STARTPTS [botv]; [0] atrim= end= bt1, asetpts=PTS-STARTPTS [bota];
    [0] trim= start= bt1, setpts=PTS-STARTPTS [uppv]; [0] atrim= start= bt1,asetpts=PTS-STARTPTS [uppa];
    
    [uppa] [1] amix [uppa_mix];
    
    [botv] [bota] [uppv] [uppa_mix] concat=n=2:v=1:a=1

*variables.FFMPEG_OUTPUT_SPECS,

output_file.mp4

"""