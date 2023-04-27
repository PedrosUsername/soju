import subprocess
import json

from .settings import variables



FFMPEG_PATH = variables.FFMPEG_PATH
FFMPEG_OUTPUT_SPECS = variables.FFMPEG_OUTPUT_SPECS
IMAGE_FOLDER = variables.DEFAULT_IMAGE_FOLDER
AUDIO_FOLDER = variables.DEFAULT_AUDIO_FOLDER
VIDEO_FOLDER = variables.DEFAULT_VIDEO_FOLDER
FFMPEG_FPS = int(variables.FFMPEG_FPS)
FFMPEG_AR = int(variables.FFMPEG_SAMPLE_RATE)
OVERLAY_SIZE_TOLERANCE = variables.OVERLAY_SIZE_TOLERANCE

















def get_only_audio(videofilepath= None, outputfilepath= "./"):
    ffmpeg = FFMPEG_PATH

    a_mapping = ["-map", "0:a"]

    ffmpegCall = [
        ffmpeg,
        "-y",
        "-i",
        videofilepath,
        *a_mapping,
        "-ac",
        "1",
        outputfilepath
    ]

    executeFfmpegCall(ffmpegCall)








def get_boomers(jsonfilepath):
    describe_json = []
    with open(jsonfilepath, 'r') as f:
        describe_json = f.read()

    return json.loads(describe_json)["boomers"]







def getBoomerImageWidth(boomer= None, main_clip_width= 0):
    if (
        not boomer
        or not boomer.get("image")
        or not boomer.get("image").get("conf")
        or not boomer.get("image").get("conf").get("width")
    ):
        return -1
    elif (main_clip_width + OVERLAY_SIZE_TOLERANCE) < boomer.get("image").get("conf").get("width"):
        return main_clip_width + OVERLAY_SIZE_TOLERANCE
    else:    
        return abs(boomer.get("image").get("conf").get("width"))
    

def getBoomerImageHeight(boomer= None, main_clip_height= 0):
    if (
        not boomer
        or not boomer.get("image")
        or not boomer.get("image").get("conf")
        or not boomer.get("image").get("conf").get("height")
    ):
        return main_clip_height + OVERLAY_SIZE_TOLERANCE
    elif (main_clip_height + OVERLAY_SIZE_TOLERANCE) < boomer.get("image").get("conf").get("height"):
        return main_clip_height + OVERLAY_SIZE_TOLERANCE
    else:    
        return abs(boomer.get("image").get("conf").get("height"))    
    

def getBoomerVideoWidth(boomer= None, main_clip_width= 0):
    if (
        not boomer
        or not boomer.get("video")
        or not boomer.get("video").get("conf")
        or not boomer.get("video").get("conf").get("width")
    ):
        return -1
    elif (main_clip_width + OVERLAY_SIZE_TOLERANCE) < boomer.get("video").get("conf").get("width"):
        return main_clip_width + OVERLAY_SIZE_TOLERANCE
    else:    
        return abs(boomer.get("video").get("conf").get("width"))
    

def getBoomerVideoHeight(boomer= None, main_clip_height= 0):
    if (
        not boomer
        or not boomer.get("video")
        or not boomer.get("video").get("conf")
        or not boomer.get("video").get("conf").get("height")
    ):
        return main_clip_height + OVERLAY_SIZE_TOLERANCE
    elif (main_clip_height + OVERLAY_SIZE_TOLERANCE) < boomer.get("video").get("conf").get("height"):
        return main_clip_height + OVERLAY_SIZE_TOLERANCE
    else:    
        return abs(boomer.get("video").get("conf").get("height"))    


def getBoomTrigger(boomer= None):
    if (
        not boomer
        or not boomer.get("word")
        or not boomer.get("word").get("trigger")
    ):
        return variables.DEFAULT_BOOM_TRIGGER if variables.DEFAULT_BOOM_TRIGGER else "end"
    else:
        return boomer.get("word").get("trigger")


def getBoomerBoominTime(boomer= None):
    trigg = getBoomTrigger(boomer)
    if (
        not boomer
        or not boomer.get("word")
        or not boomer.get("word").get(trigg)
    ):
        return 0
    else:
        return float(boomer.get("word").get(trigg))


def getBoomerImageDuration(boomer= None):
    if (
        not boomer
        or not boomer.get("image") 
        or not boomer.get("image").get("conf")
        or not boomer.get("image").get("conf").get("duration")
    ):
        return 0
    else:
        return boomer.get("image").get("conf").get("duration")


def getBoomerAudioDuration(boomer= None):
    if (
        not boomer
        or not boomer.get("audio") 
        or not boomer.get("audio").get("conf")
        or not boomer.get("audio").get("conf").get("duration")
    ):
        return 0
    else:
        return boomer.get("audio").get("conf").get("duration")
    

def getBoomerVideoDuration(boomer= None):
    if (
        not boomer
        or not boomer.get("video") 
        or not boomer.get("video").get("conf")
        or not boomer.get("video").get("conf").get("duration")
    ):
        return 0
    else:
        return boomer.get("video").get("conf").get("duration")


def getBoomerVideoVolume(boomer= None):
    if (
        not boomer
        or not boomer.get("video")
        or not boomer.get("video").get("conf")
        or not boomer.get("video").get("conf").get("volume")
    ):
        if boomer.get("video").get("conf").get("volume") == 0:
            return 0
        else:
            return 1
    else:
        return boomer.get("video").get("conf").get("volume")
    

def getBoomerAudioVolume(boomer= None):
    if (
        not boomer
        or not boomer.get("video")
        or not boomer.get("video").get("conf")
        or not boomer.get("audio").get("conf").get("volume")
    ):
        if boomer.get("audio").get("conf").get("volume") == 0:
            return 0
        else:
            return 1
    else:
        return boomer.get("audio").get("conf").get("volume")    


def classifyImageFiles(image_files):
    image_files_compose = []
    image_files_concat = []

    for b in image_files:
        if (
            b.get("image").get("conf")
            and b.get("image").get("conf").get("mergestrategy") == "COMPOSE"
        ):
            image_files_compose = image_files_compose + [b]
        elif(
            b.get("image").get("conf")
            and b.get("image").get("conf").get("mergestrategy") == "CONCAT"
        ):
            image_files_concat = image_files_concat + [b]

    return (image_files_compose, image_files_concat)


def classifyVideoFiles(video_files):
    video_files_compose = []
    video_files_concat = []

    for b in video_files:
        if (
            b.get("video").get("conf")
            and b.get("video").get("conf").get("mergestrategy") == "COMPOSE"
        ):
            video_files_compose = video_files_compose + [b]
        elif(
            b.get("video").get("conf")
            and b.get("video").get("conf").get("mergestrategy") == "CONCAT"
        ):
            video_files_concat = video_files_concat + [b]

    return (video_files_compose, video_files_concat)





















def executeFfmpegCall(params= []):
    subprocess.run(
        params
    )


def cleanFilterParams(params= "", filth= ""):
    return params[:(len(filth) * -1)]


def buildCall(main_clip_params, outputfilepath= "output.mp4", boomers= None):
    ffmpeg = FFMPEG_PATH
    output_specs = FFMPEG_OUTPUT_SPECS

    main_clip_file = main_clip_params.get("file")

    video_files = [ b for b in boomers if b.get("video") and b.get("video").get("file") ]
    image_files = [ b for b in boomers if b.get("image") and b.get("image").get("file") ]
    audio_files = [ b for b in boomers if b.get("audio") and b.get("audio").get("file") ]

    video_files_compose, video_files_concat = classifyVideoFiles(video_files)
    image_files_compose, image_files_concat = classifyImageFiles(image_files)

    video_files_concat.sort(key= getBoomerBoominTime, reverse= True)
    image_files_concat.sort(key= getBoomerBoominTime, reverse= True)



    media_inputs = buildMediaInputs(
        video_files_compose= video_files_compose,
        image_files_compose= image_files_compose,
        audio_files= audio_files,
        video_files_concat= video_files_concat,
        image_files_concat= image_files_concat
    )

    v_mapping = ["-map", "0:v"]
    a_mapping = ["-map", "0:a"]

    filter_params_label = "-filter_complex"
    filter_params = ""
    
    separator = "; "

    if len(video_files_compose) > 0:
        main_label = "[0]"
        fout_label_v = "[outv]"
        fout_label_a = "[outa]"

        filter_params = (
            filter_params
            + buildVideoOverlayFilterParams (
                video_files_compose,
                inp= main_label,
                out_v= fout_label_v,
                out_a= fout_label_a,
                first_file_idx= 1,
                main_clip_params= main_clip_params
            )
            + fout_label_v
            + fout_label_a
            + separator            
        )

        v_mapping = ["-map", fout_label_v]
        a_mapping = ["-map", fout_label_a]


    if len(image_files_compose) > 0:
        main_label = "[outv]" if len(video_files_compose) > 0 else "[0]"
        fout_label = "[outv]"

        filter_params = (
            filter_params
            + buildImageOverlayFilterParams (
                image_files_compose,
                inp= main_label,
                out= fout_label,
                first_file_idx= len(video_files_compose) + 1,
                main_clip_params= main_clip_params
            )
            + fout_label
            + separator
        )

        v_mapping = ["-map", fout_label]


    if len(audio_files) > 0:
        main_label =  "[outa]" if len(video_files_compose) > 0 else "[0]"
        fout_label = "[outa]"

        filter_params = (
            filter_params
            + buildAudioAmixFilterParams (
                audio_files,
                inp= main_label,
                out= fout_label,
                first_file_idx= len(video_files_compose) + len(image_files_compose) + 1
            )
            + fout_label
            + separator
        )

        a_mapping = ["-map", fout_label]

    
    if len(video_files_concat) > 0:
        main_label_v = "[outv]" if (len(video_files_compose) + len(image_files_compose)) > 0 else "[0]"
        main_label_a = "[outa]" if (len(video_files_compose) + len(audio_files)) > 0 else "[0]"
        fout_label_v = "[outv]"
        fout_label_a = "[outa]"

        filter_params = (
            filter_params
            + buildVideoConcatFilterParams (
                video_files_concat,
                inp_v= main_label_v,
                inp_a= main_label_a,                
                out_v= fout_label_v,
                out_a= fout_label_a,
                first_file_idx= len(video_files_compose) + len(image_files_compose) + len(audio_files) + 1,
                main_clip_params= main_clip_params
            )
            + fout_label_v
            + fout_label_a
            + separator            
        )

        v_mapping = ["-map", fout_label_v]
        a_mapping = ["-map", fout_label_a]



    if len(image_files_concat) > 0:
        main_label_v = "[outv]" if (len(video_files_concat) + len(video_files_compose) + len(image_files_compose)) > 0 else "[0]"
        main_label_a = "[outa]" if (len(video_files_concat) + len(video_files_compose) + len(audio_files)) > 0 else "[0]"
        fout_label_v = "[outv]"
        fout_label_a = "[outa]"

        filter_params = (
            filter_params
            + buildImageConcatFilterParams (
                image_files_concat,
                inp_v= main_label_v,
                inp_a= main_label_a,                
                out_v= fout_label_v,
                out_a= fout_label_a,
                first_file_idx= len(video_files_concat) + len(video_files_compose) + len(image_files_compose) + len(audio_files) + 1,
                main_clip_params= main_clip_params
            )
            + fout_label_v
            + fout_label_a
            + separator            
        )

        v_mapping = ["-map", fout_label_v]
        a_mapping = ["-map", fout_label_a]        
    

    filter_params = cleanFilterParams(filter_params, filth= separator)

    ffmpegCall = [
        ffmpeg,
        "-y",
        "-i",
        main_clip_file,
        *media_inputs
    ]

    if (len(media_inputs) > 0):
        ffmpegCall = ffmpegCall + [
            filter_params_label,
            filter_params
        ]
        
    ffmpegCall = ffmpegCall + [
        *v_mapping,
        *a_mapping,
        *output_specs,
        outputfilepath
    ]

    return ffmpegCall









def buildMediaInputs(
        video_files_compose= [],
        video_files_concat= [],
        image_files_compose= [],
        image_files_concat= [],
        audio_files= []
):
    media_inputs = []
    
    for file in video_files_compose:
        media_inputs = media_inputs + ["-i"] + [VIDEO_FOLDER + file["video"]["file"]]

    for file in image_files_compose:
        media_inputs = media_inputs + ["-i"] + [IMAGE_FOLDER + file["image"]["file"]]

    for file in audio_files:
        media_inputs = media_inputs + ["-i"] + [AUDIO_FOLDER + file["audio"]["file"]]

    for file in video_files_concat:
        media_inputs = media_inputs + ["-i"] + [VIDEO_FOLDER + file["video"]["file"]]

    for file in image_files_concat:
        media_inputs = media_inputs + ["-i"] + [IMAGE_FOLDER + file["image"]["file"]]        


    return media_inputs







def buildImageOverlayFilterParams(boomers= [], inp= "[0]", out= "[outv]", first_file_idx= 0, main_clip_params= {}):
    filter_params = ""
    main_clip_width = main_clip_params.get("width") if main_clip_params.get("width") else 0
    main_clip_height = main_clip_params.get("height") if main_clip_params.get("height") else 0

    head = boomers[:1]
    for boomer in head:
        img_width = getBoomerImageWidth(boomer, main_clip_width)
        img_height = getBoomerImageHeight(boomer, main_clip_height)

        boomin_time_start = getBoomerBoominTime(boomer)
        boomin_time_end = boomin_time_start + getBoomerImageDuration(boomer)
        filter_params = filter_params + """
[{1}] scale= w= {4}:h= {5} [img];
{0}[img] overlay= x=main_w/2-overlay_w/2:y=main_h/2-overlay_h/2:enable='between(t, {2}, {3})', setpts=PTS-STARTPTS, setsar=1
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
        img_width = getBoomerImageWidth(boomer, main_clip_width)
        img_height = getBoomerImageHeight(boomer, main_clip_height)        
        boomin_time_start = getBoomerBoominTime(boomer)
        boomin_time_end = boomin_time_start + getBoomerImageDuration(boomer)
        filter_params = filter_params + """{0};
[{1}] scale= w= {4}:h= {5} [img];
{0}[img] overlay= x=main_w/2-overlay_w/2:y=main_h/2-overlay_h/2:enable='between(t, {2}, {3})', setpts=PTS-STARTPTS, setsar=1
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
        duration = getBoomerAudioDuration(boomer)
        volume = getBoomerAudioVolume(boomer)

        filter_params = filter_params + """
{0} asplit=2
[fin2] [fin4];

[fin2] atrim= end= {2}, asetpts=PTS-STARTPTS
[bota];

[fin4] atrim= start= {2}, asetpts=PTS-STARTPTS
[uppa];

[{1}] atrim= end= {3}, volume= {4}, asetpts=PTS-STARTPTS
[aud];

[uppa] [aud] amix= dropout_transition=0, dynaudnorm
[uppa_mix];

[bota] [uppa_mix] concat=n=2:v=0:a=1
""".format(
            inp,
            first_file_idx,
            boomin_time_start,
            duration,
            volume
        )

    tail = boomers[1:]
    for idx, boomer in enumerate(tail, first_file_idx + 1):
        boomin_time_start = getBoomerBoominTime(boomer)
        duration = getBoomerAudioDuration(boomer)
        volume = getBoomerAudioVolume(boomer)

        filter_params = filter_params + """{0};
{0} asplit=2
[outa1] [outa2];

[outa1] atrim= end= {2}, asetpts=PTS-STARTPTS
[bota];

[outa2] atrim= start= {2},asetpts=PTS-STARTPTS
[uppa];

[{1}] atrim= end= {3}, volume= {4}, asetpts=PTS-STARTPTS
[aud];

[uppa] [aud] amix= dropout_transition=0, dynaudnorm
[uppa_mix];

[bota] [uppa_mix] concat=n=2:v=0:a=1
""".format(
        out,
        idx,
        boomin_time_start,
        duration,
        volume
    )        
        
    return filter_params



def buildVideoOverlayFilterParams(boomers= [], inp= "[0]", out_v= "[outv]", out_a= "[outa]", first_file_idx= 0, main_clip_params= {}):
    filter_params = ""
    main_clip_width = main_clip_params.get("width") if main_clip_params.get("width") else 0
    main_clip_height = main_clip_params.get("height") if main_clip_params.get("height") else 0

    head = boomers[:1]
    for boomer in head:
        vid_width = getBoomerVideoWidth(boomer, main_clip_width)
        vid_height = getBoomerVideoHeight(boomer, main_clip_height)

        boomin_time_start = getBoomerBoominTime(boomer)
        duration = getBoomerVideoDuration(boomer)
        volume = getBoomerVideoVolume(boomer)
        filter_params = filter_params + """        

{0} split=2 
[fin1] [fin3];

[fin1] trim= end= {2}, setpts=PTS-STARTPTS
[botv];

[fin3] trim= start= {2}, setpts=PTS-STARTPTS
[uppv];

[{1}] trim= end= {3}, scale= w= {4}:h= {5}, setpts=PTS-STARTPTS
[b_video];

[uppv] [b_video] overlay= x=main_w/2-overlay_w/2:y=main_h/2-overlay_h/2:enable='between(t, 0, {3})'
[uppv_mix];

{0} asplit=2 
[fin2] [fin4];

[fin2] atrim= end= {2}, asetpts=PTS-STARTPTS
[bota];

[fin4] atrim= start= {2}, asetpts=PTS-STARTPTS
[uppa];

[{1}] atrim= end= {3}, volume= {6}, asetpts=PTS-STARTPTS
[b_audio];

[uppa] [b_audio] amix= dropout_transition=0, dynaudnorm
[uppa_mix];
 
[botv] [bota] [uppv_mix] [uppa_mix] concat=n=2:v=1:a=1
""".format(
            inp,
            first_file_idx,
            boomin_time_start,
            duration,
            vid_width,
            vid_height,
            volume
        )

    tail = boomers[1:]
    for idx, boomer in enumerate(tail, first_file_idx + 1):
        vid_width = getBoomerVideoWidth(boomer, main_clip_width)
        vid_height = getBoomerVideoHeight(boomer, main_clip_height)     

        boomin_time_start = getBoomerBoominTime(boomer)
        duration = getBoomerVideoDuration(boomer)
        volume = getBoomerVideoVolume(boomer)        
        filter_params = filter_params + """{0}{6};

{0} split=2 
[fin1] [fin3];

[fin1] trim= end= {2}, setpts=PTS-STARTPTS
[botv];

[fin3] trim= start= {2}, setpts=PTS-STARTPTS
[uppv];

[{1}] trim= end= {3}, scale= w= {4}:h= {5}, setpts=PTS-STARTPTS
[b_video];

[uppv] [b_video] overlay= x=main_w/2-overlay_w/2:y=main_h/2-overlay_h/2:enable='between(t, 0, {3})'
[uppv_mix];

{6} asplit=2 
[fin2] [fin4];

[fin2] atrim= end= {2}, asetpts=PTS-STARTPTS
[bota];

[fin4] atrim= start= {2}, asetpts=PTS-STARTPTS
[uppa];

[{1}] atrim= end= {3}, volume= {7}, asetpts=PTS-STARTPTS
[b_audio];

[uppa] [b_audio] amix= dropout_transition=0, dynaudnorm
[uppa_mix];
 
[botv] [bota] [uppv_mix] [uppa_mix] concat=n=2:v=1:a=1
""".format(
            out_v,
            idx,
            boomin_time_start,
            duration,
            vid_width,
            vid_height,
            out_a,
            volume
        )

    return filter_params





def buildVideoConcatFilterParams(boomers= [], inp_v= "[0]", inp_a= "[0]", out_v= "[outv]", out_a= "[outa]", first_file_idx= 0, main_clip_params= {}):
    filter_params = ""
    main_clip_width = main_clip_params.get("width") if main_clip_params.get("width") else 0
    main_clip_height = main_clip_params.get("height") if main_clip_params.get("height") else 0

    duration = 0

    head = boomers[:1]
    for boomer in head:
        boomin_time_start = getBoomerBoominTime(boomer)
        duration = getBoomerVideoDuration(boomer)
        volume = getBoomerVideoVolume(boomer)

        filter_params = filter_params + f"""
{inp_v} split=2 
[fin1] [fin3];

[fin1] trim= end= {boomin_time_start}, setpts=PTS-STARTPTS, setsar=1
[botv];

[fin3] trim= start= {boomin_time_start}, setpts=PTS-STARTPTS, setsar=1
[uppv];

{inp_a} asplit=2 
[fin2] [fin4];

[fin2] atrim= end= {boomin_time_start}, asetpts=PTS-STARTPTS
[bota];

[fin4] atrim= start= {boomin_time_start}, asetpts=PTS-STARTPTS
[uppa];

[{first_file_idx}] trim= end= {duration}, scale=w={main_clip_width}:h={main_clip_height}, setpts=PTS-STARTPTS, setsar=1
[vid];

[{first_file_idx}] atrim= end= {duration}, volume= {volume}, asetpts=PTS-STARTPTS
[aud];

[botv] [bota] [vid] [aud] [uppv] [uppa] concat=n=3:v=1:a=1
"""

    tail = boomers[1:]


    for idx, boomer in enumerate(tail, first_file_idx + 1):

        boomin_time_start = getBoomerBoominTime(boomer)
        duration = getBoomerVideoDuration(boomer)
        volume = getBoomerVideoVolume(boomer)

        filter_params = filter_params + f"""{out_v}{out_a};


        
{out_v} split=2 
[fin1] [fin3];

[fin1] trim= end= {boomin_time_start}, setpts=PTS-STARTPTS, setsar=1
[botv];

[fin3] trim= start= {boomin_time_start}, setpts=PTS-STARTPTS, setsar=1
[uppv];

{out_a} asplit=2 
[fin2] [fin4];

[fin2] atrim= end= {boomin_time_start}, asetpts=PTS-STARTPTS
[bota];

[fin4] atrim= start= {boomin_time_start}, asetpts=PTS-STARTPTS
[uppa];

[{idx}] trim= end= {duration}, scale=w={main_clip_width}:h={main_clip_height}, setpts=PTS-STARTPTS, setsar=1
[vid];

[{idx}] atrim= end= {duration}, volume= {volume}, asetpts=PTS-STARTPTS
[aud];

[botv] [bota] [vid] [aud] [uppv] [uppa] concat=n=3:v=1:a=1
"""

    return filter_params    





def buildImageConcatFilterParams(boomers= [], inp_v= "[0]", inp_a= "[0]", out_v= "[outv]", out_a= "[outa]", first_file_idx= 0, main_clip_params= {}):
    filter_params = ""
    main_clip_width = main_clip_params.get("width") if main_clip_params.get("width") else 0
    main_clip_height = main_clip_params.get("height") if main_clip_params.get("height") else 0

    duration = 0

    head = boomers[:1]
    for boomer in head:
        boomin_time_start = getBoomerBoominTime(boomer)
        duration = getBoomerImageDuration(boomer)

        filter_params = filter_params + f"""
{inp_v} split=2 
[fin1] [fin3];

[fin1] trim= end= {boomin_time_start}, setpts=PTS-STARTPTS, setsar=1
[botv];

[fin3] trim= start= {boomin_time_start}, setpts=PTS-STARTPTS, setsar=1
[uppv];

{inp_a} asplit=2 
[fin2] [fin4];

[fin2] atrim= end= {boomin_time_start}, asetpts=PTS-STARTPTS
[bota];

[fin4] atrim= start= {boomin_time_start}, asetpts=PTS-STARTPTS
[uppa];

[{first_file_idx}] loop= loop=-1:size=1:start=0, trim= end= {duration}, scale=w={main_clip_width}:h={main_clip_height}, setpts=PTS-STARTPTS, setsar=1
[vid];

anullsrc=r=44100:cl=mono, atrim= end= {duration}
[aud];

[botv] [bota] [vid] [aud] [uppv] [uppa] concat=n=3:v=1:a=1
"""

    tail = boomers[1:]


    for idx, boomer in enumerate(tail, first_file_idx + 1):

        boomin_time_start = getBoomerBoominTime(boomer)
        duration = getBoomerImageDuration(boomer)

        filter_params = filter_params + f"""{out_v}{out_a};


        
{out_v} split=2 
[fin1] [fin3];

[fin1] trim= end= {boomin_time_start}, setpts=PTS-STARTPTS, setsar=1
[botv];

[fin3] trim= start= {boomin_time_start}, setpts=PTS-STARTPTS, setsar=1
[uppv];

{out_a} asplit=2 
[fin2] [fin4];

[fin2] atrim= end= {boomin_time_start}, asetpts=PTS-STARTPTS
[bota];

[fin4] atrim= start= {boomin_time_start}, asetpts=PTS-STARTPTS
[uppa];

[{idx}] loop= loop=-1:size=1:start=0, trim= end= {duration}, scale=w={main_clip_width}:h={main_clip_height}, setpts=PTS-STARTPTS, setsar=1
[vid];

anullsrc=r=44100:cl=mono, atrim= end= {duration}
[aud];

[botv] [bota] [vid] [aud] [uppv] [uppa] concat=n=3:v=1:a=1
"""

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
concat video-video
ffmpeg -i assets/video/vox.mp4 -i assets/video/clips/therock_sus.mp4 -filter_complex "[0:v]scale=w=1920:h=1080, setsar=1, setpts=PTS-STARTPTS [v0]; [1:v]scale=w=1920:h=1080, setsar=1, setpts=PTS-STARTPTS [v1]; [v0][0:a][v1][1:a] concat=n=2:v=1:a=1 [v] [a]" -map "[v]" -map "[a]"  -r 30 -c:v h264 -c:a mp3 -b:v 64k -b:a 196k -ar 44100 -preset fast -crf 22 -s 1280x720 -pix_fmt yuv420p -video_track_timescale 90000 out.mp4
concat video-img
ffmpeg -i assets/video/vox.mp4 -i assets/image/cursed/dog.jpg -filter_complex "[0:v]scale=w=1920:h=1080, setsar=1, setpts=PTS-STARTPTS [v0]; [1:v]scale=w=1920:h=1080, loop=loop=60:size=1:start=0, setsar=1, setpts=PTS-STARTPTS [v1]; [v0][v1] concat=n=2:v=1:a=0 [v]" -map "[v]" -map 0:a -r 30 -c:v h264 -c:a mp3 -b:v 64k -b:a 196k -ar 44100 -preset fast -crf 22 -s 1280x720 -pix_fmt yuv420p -video_track_timescale 90000 out.mp4
"""


