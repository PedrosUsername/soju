import subprocess
import random

from .settings import variables
from . import moviepy_utils as mu, boomer_utils as bu
from .enum.Enum import ImageFilesDir, VideoFilesDir, AudioFilesDir, MergeStrategy, Position



FFMPEG_PATH = variables.FFMPEG_PATH
FFMPEG_OUTPUT_SPECS = variables.FFMPEG_OUTPUT_SPECS
FFMPEG_FPS = int(variables.FFMPEG_FPS)
FFMPEG_AR = int(variables.FFMPEG_SAMPLE_RATE)
OVERLAY_SIZE_TOLERANCE = variables.OVERLAY_SIZE_TOLERANCE








































def get_only_audio(videofilepath= None, outputfilepath= "./"):
    ffmpeg = FFMPEG_PATH

    a_mapping = ["-map", "0:a?"]

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


































def extend_boomers_by_video_concaters(boomers= []) :
    boomers.sort(key= bu.getBoomerBoominTimeForFFMPEG)
    new_bmrs = []

    accumulator = 0
    for b in boomers :
        video_mergestrategy = bu.getBoomerVideoMergeStrategyForFFMPEG(b)

        image_duration = bu.getBoomerImageDurationForFFMPEG(b)
        video_duration = bu.getBoomerVideoDurationForFFMPEG(b)
        audio_duration = bu.getBoomerAudioDurationForFFMPEG(b)

        btrigger = bu.getBoomTrigger(b)

        if (
            btrigger is not None
            and b.get("word")
            and b.get("word").get(btrigger)
        ) :
            if image_duration is not None or video_duration is not None or audio_duration is not None :
                b["word"][btrigger] = b["word"][btrigger] + accumulator

        if video_mergestrategy == MergeStrategy.get("CONCAT") :
            accumulator = (accumulator + video_duration) if video_duration is not None else accumulator

        new_bmrs = new_bmrs + [b]

    return new_bmrs





def extend_boomers_by_image_concaters(boomers= []) :
    boomers.sort(key= bu.getBoomerBoominTimeForFFMPEG)
    new_bmrs = []

    accumulator = 0
    for b in boomers :
        image_mergestrategy = bu.getBoomerImageMergeStrategyForFFMPEG(b)

        image_duration = bu.getBoomerImageDurationForFFMPEG(b)
        video_duration = bu.getBoomerVideoDurationForFFMPEG(b)
        audio_duration = bu.getBoomerAudioDurationForFFMPEG(b)

        btrigger = bu.getBoomTrigger(b)

        if (
            btrigger is not None
            and b.get("word")
            and b.get("word").get(btrigger)
        ) :
            if image_duration is not None or video_duration is not None or audio_duration is not None :
                b["word"][btrigger] = b["word"][btrigger] + accumulator

        if image_mergestrategy == MergeStrategy.get("CONCAT") :
            accumulator = (accumulator + image_duration) if image_duration is not None else accumulator

        new_bmrs = new_bmrs + [b]

    return new_bmrs




def executeFfmpegCall(params= []):
    subprocess.run(
        params
    )


def cleanFilterParams(params= "", filth= ""):
    return params[:(len(filth) * -1)]


def buildCall(outputfilepath= "output.mp4", boomers= None):
    ffmpeg = FFMPEG_PATH
    output_specs = FFMPEG_OUTPUT_SPECS
    main_clip_params = mu.get_og_clip_params()

    main_clip_file = main_clip_params.get("file")

    video_files = [ b for b in extend_boomers_by_video_concaters(boomers) if b.get("video") and b.get("video").get("file") ]

    video_files_compose, video_files_concat = bu.classifyBoomersByVideoMergeStrategy(video_files)


    v_mapping = ["-map", "0:v"]
    a_mapping = ["-map", "0:a"]

    main_label_v = "[0]"
    main_label_a = "[0]"
    fout_label_v = "[outv]"
    fout_label_a = "[outa]"

    filter_params_label = "-filter_complex"
    filter_params = ""
    
    separator = "; "

    first_file_idx = 1
    if len(video_files_concat) > 0:

        filter_params = (
            filter_params
            + buildVideoConcatFilterParams (
                video_files_concat,
                inp_v= main_label_v,
                inp_a= main_label_a,                
                out_v= fout_label_v,
                out_a= fout_label_a,
                first_file_idx= first_file_idx,
                main_clip_params= main_clip_params
            )
            + fout_label_v
            + fout_label_a
            + separator            
        )

        v_mapping = ["-map", fout_label_v]
        a_mapping = ["-map", fout_label_a]

        main_label_v = fout_label_v
        main_label_a = fout_label_a


    boomers = extend_boomers_by_image_concaters(boomers)

    video_files = [ b for b in boomers if b.get("video") and b.get("video").get("file") ]
    image_files = [ b for b in boomers if b.get("image") and b.get("image").get("file") ]
    audio_files = [ b for b in boomers if b.get("audio") and b.get("audio").get("file") ]

    video_files_compose, video_files_concat = bu.classifyBoomersByVideoMergeStrategy(video_files)
    image_files_compose, image_files_concat = bu.classifyBoomersByImageMergeStrategy(image_files)



    first_file_idx = first_file_idx + len(video_files_concat)
    if len(image_files_concat) > 0:

        filter_params = (
            filter_params
            + buildImageConcatFilterParams (
                image_files_concat,
                inp_v= main_label_v,
                inp_a= main_label_a,                
                out_v= fout_label_v,
                out_a= fout_label_a,
                first_file_idx= first_file_idx,
                main_clip_params= main_clip_params
            )
            + fout_label_v
            + fout_label_a
            + separator            
        )

        v_mapping = ["-map", fout_label_v]
        a_mapping = ["-map", fout_label_a]        

        main_label_v = fout_label_v
        main_label_a = fout_label_a



    first_file_idx = first_file_idx + len(image_files_concat)
    if len(video_files_compose) > 0:

        filter_params = (
            filter_params
            + buildVideoOverlayFilterParams (
                video_files_compose,
                inp_v= main_label_v,
                inp_a= main_label_a,                
                out_v= fout_label_v,
                out_a= fout_label_a,
                first_file_idx= first_file_idx,
                main_clip_params= main_clip_params
            )
            + fout_label_v
            + fout_label_a
            + separator            
        )

        v_mapping = ["-map", fout_label_v]
        a_mapping = ["-map", fout_label_a]

        main_label_v = fout_label_v
        main_label_a = fout_label_a




    first_file_idx = first_file_idx + len(video_files_compose)
    if len(image_files_compose) > 0:

        filter_params = (
            filter_params
            + buildImageOverlayFilterParams (
                image_files_compose,
                inp= main_label_v,
                out= fout_label_v,
                first_file_idx= first_file_idx,
                main_clip_params= main_clip_params
            )
            + fout_label_v
            + separator
        )

        v_mapping = ["-map", fout_label_v]

        main_label_v = fout_label_v


    first_file_idx = first_file_idx + len(image_files_compose)
    if len(audio_files) > 0:

        filter_params = (
            filter_params
            + buildAudioAmixFilterParams (
                audio_files,
                inp= main_label_a,
                out= fout_label_a,
                first_file_idx= first_file_idx
            )
            + fout_label_a
            + separator
        )

        a_mapping = ["-map", fout_label_a]

        main_label_a = fout_label_a

    filter_params = cleanFilterParams(filter_params, filth= separator)

    media_inputs = buildMediaInputs(
        video_files_compose= video_files_compose,
        image_files_compose= image_files_compose,
        audio_files= audio_files,
        video_files_concat= video_files_concat,
        image_files_concat= image_files_concat
    )

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

    for file in video_files_concat:
        file_name = VideoFilesDir.get(bu.getBoomerDefaultVideoDirForFFMPEG(file)) + file["video"]["file"] if not file["video"]["file"].startswith("https://") else file["video"]["file"]        
        media_inputs = media_inputs + ["-i"] + [file_name]

    for file in image_files_concat:
        file_name = ImageFilesDir.get(bu.getBoomerDefaultImageDirForFFMPEG(file)) + file["image"]["file"] if not file["image"]["file"].startswith("https://") else file["image"]["file"]        
        media_inputs = media_inputs + ["-i"] + [file_name]

    for file in video_files_compose:
        file_name = VideoFilesDir.get(bu.getBoomerDefaultVideoDirForFFMPEG(file)) + file["video"]["file"] if not file["video"]["file"].startswith("https://") else file["video"]["file"]
        media_inputs = media_inputs + ["-i"] + [file_name]

    for file in image_files_compose:
        file_name = ImageFilesDir.get(bu.getBoomerDefaultImageDirForFFMPEG(file)) + file["image"]["file"] if not file["image"]["file"].startswith("https://") else file["image"]["file"]        
        media_inputs = media_inputs + ["-i"] + [file_name]

    for file in audio_files:
        file_name = AudioFilesDir.get(bu.getBoomerDefaultAudioDirForFFMPEG(file)) + file["audio"]["file"] if not file["audio"]["file"].startswith("https://") else file["audio"]["file"]        
        media_inputs = media_inputs + ["-i"] + [file_name]        


    return media_inputs







def buildImageOverlayFilterParams(boomers= [], inp= "[0]", out= "[outv]", first_file_idx= 0, main_clip_params= {}):
    filter_params = ""
    main_clip_width = main_clip_params.get("width") if main_clip_params.get("width") else 0
    main_clip_height = main_clip_params.get("height") if main_clip_params.get("height") else 0

    head = boomers[:1]
    for boomer in head:
        img_width = bu.getBoomerImageWidthForFFMPEG(boomer, main_clip_width)
        img_height = bu.getBoomerImageHeightForFFMPEG(boomer, main_clip_height)

        positionx = bu.getBoomerImagePosXForFFMPEG(boomer)
        positiony = bu.getBoomerImagePosYForFFMPEG(boomer)        

        if positionx == Position.get("TOP") :
            posx = "x=main_w-overlay_w-12"
        elif positionx == Position.get("CENTER") :
            posx = "x=main_w/2-overlay_w/2"
        elif positionx == Position.get("BOTTOM") :
            posx = "x=12"
        elif positionx == Position.get("RANDOM") :
            if main_clip_width and img_width :
                randomx = random.choice(range(int(float(0.8 * main_clip_width - img_width))))
            elif main_clip_width and img_height :
                randomx = random.choice(range(int(float(0.8 * main_clip_width - img_height))))
            else :
                randomx = 12
            for _ in range(8) :
                print(f"randomx: {randomx}, main_w: {main_clip_width}, img_w: {img_width}", end="\n")
            posx = "x={}".format(randomx)            

        if positiony == Position.get("TOP") :
            posy = "y=12"
        elif positiony == Position.get("CENTER") :
            posy = "y=main_h/2-overlay_h/2"
        elif positiony == Position.get("BOTTOM") :
            posy = "y=main_h-overlay_h-12"
        elif positiony == Position.get("RANDOM") :
            if main_clip_height and img_height :
                randomy = random.choice(range(main_clip_height - img_height))
            else :
                randomy = 12
            for _ in range(8) :
                print(f"randomy: {randomy}, main_h: {main_clip_height}, img_h: {img_height}", end="\n")
            posy = "y={}".format(randomy)            

        boomin_time_start = bu.getBoomerBoominTimeForFFMPEG(boomer)
        boomin_time_end = boomin_time_start + bu.getBoomerImageDurationForFFMPEG(boomer)
        filter_params = filter_params + """
[{1}] scale= w= {4}:h= {5} [img];
{0}[img] overlay= {6}:{7}:enable='between(t, {2}, {3})', setpts=PTS-STARTPTS, setsar=1
""".format(
            inp,
            first_file_idx,
            boomin_time_start,
            boomin_time_end,
            img_width if img_width else -1,
            img_height if img_height else -1,
            posx,
            posy
        )

    tail = boomers[1:]
    for idx, boomer in enumerate(tail, first_file_idx + 1):
        img_width = bu.getBoomerImageWidthForFFMPEG(boomer, main_clip_width)
        img_height = bu.getBoomerImageHeightForFFMPEG(boomer, main_clip_height)        

        positionx = bu.getBoomerImagePosXForFFMPEG(boomer)
        positiony = bu.getBoomerImagePosYForFFMPEG(boomer)        

        if positionx == Position.get("TOP") :
            posx = "x=main_w-overlay_w-12"
        elif positionx == Position.get("CENTER") :
            posx = "x=main_w/2-overlay_w/2"
        elif positionx == Position.get("BOTTOM") :
            posx = "x=12"
        elif positionx == Position.get("RANDOM") :
            if main_clip_width and img_width :
                randomx = random.choice(range(int(float(0.8 * main_clip_width - img_width))))
            elif main_clip_width and img_height :
                randomx = random.choice(range(int(float(0.8 * main_clip_width - img_height))))
            else :
                randomx = 12

            posx = "x={}".format(randomx)            

        if positiony == Position.get("TOP") :
            posy = "y=12"
        elif positiony == Position.get("CENTER") :
            posy = "y=main_h/2-overlay_h/2"
        elif positiony == Position.get("BOTTOM") :
            posy = "y=main_h-overlay_h-12"
        elif positiony == Position.get("RANDOM") :
            if main_clip_height and img_height :
                randomy = random.choice(range(main_clip_height - img_height))
            else :
                randomy = 12

            posy = "y={}".format(randomy)            


        boomin_time_start = bu.getBoomerBoominTimeForFFMPEG(boomer)
        boomin_time_end = boomin_time_start + bu.getBoomerImageDurationForFFMPEG(boomer)
        filter_params = filter_params + """{0};
[{1}] scale= w= {4}:h= {5} [img];
{0}[img] overlay= {6}:{7}:enable='between(t, {2}, {3})', setpts=PTS-STARTPTS, setsar=1
""".format(
            out,
            idx,
            boomin_time_start,
            boomin_time_end,
            img_width if img_width else -1,
            img_height if img_height else -1,
            posx,
            posy
        )

    return filter_params











def buildAudioAmixFilterParams(boomers= [], inp= "[0]", out= "[outa]", first_file_idx= 0):
    filter_params = ""

    head = boomers[:1]
    for boomer in head:
        boomin_time_start = bu.getBoomerBoominTimeForFFMPEG(boomer)
        duration = bu.getBoomerAudioDurationForFFMPEG(boomer)
        volume = bu.getBoomerAudioVolumeForFFMPEG(boomer)

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
        boomin_time_start = bu.getBoomerBoominTimeForFFMPEG(boomer)
        duration = bu.getBoomerAudioDurationForFFMPEG(boomer)
        volume = bu.getBoomerAudioVolumeForFFMPEG(boomer)

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



def buildVideoOverlayFilterParams(boomers= [], inp_v= "[0]", inp_a= "[0]", out_v= "[outv]", out_a= "[outa]", first_file_idx= 0, main_clip_params= {}):
    filter_params = ""
    main_clip_width = main_clip_params.get("width") if main_clip_params.get("width") else 0
    main_clip_height = main_clip_params.get("height") if main_clip_params.get("height") else 0

    head = boomers[:1]
    for boomer in head:
        vid_width = bu.getBoomerVideoWidthForFFMPEG(boomer, main_clip_width)
        vid_height = bu.getBoomerVideoHeightForFFMPEG(boomer, main_clip_height)

        positionx = bu.getBoomerVideoPosXForFFMPEG(boomer)
        positiony = bu.getBoomerVideoPosYForFFMPEG(boomer)        

        if positionx == Position.get("TOP") :
            posx = "x=main_w-overlay_w-12"
        elif positionx == Position.get("CENTER") :
            posx = "x=main_w/2-overlay_w/2"
        elif positionx == Position.get("BOTTOM") :
            posx = "x=12"
        elif positionx == Position.get("RANDOM") :
            if main_clip_width and vid_width :
                randomx = random.choice(range(int(float(0.8 * main_clip_width - vid_width))))
            elif main_clip_width and vid_height :
                randomx = random.choice(range(int(float(0.8 * main_clip_width - vid_height))))
            else :
                randomx = 12
            for _ in range(8) :
                print(f"randomx: {randomx}, main_w: {main_clip_width}, img_w: {vid_width}", end="\n")
            posx = "x={}".format(randomx)            

        if positiony == Position.get("TOP") :
            posy = "y=12"
        elif positiony == Position.get("CENTER") :
            posy = "y=main_h/2-overlay_h/2"
        elif positiony == Position.get("BOTTOM") :
            posy = "y=main_h-overlay_h-12"
        elif positiony == Position.get("RANDOM") :
            if main_clip_height and vid_height :
                randomy = random.choice(range(main_clip_height - vid_height))
            else :
                randomy = 12
            for _ in range(8) :
                print(f"randomy: {randomy}, main_h: {main_clip_height}, img_h: {vid_height}", end="\n")
            posy = "y={}".format(randomy)            

        boomin_time_start = bu.getBoomerBoominTimeForFFMPEG(boomer)
        duration = bu.getBoomerVideoDurationForFFMPEG(boomer)
        volume = bu.getBoomerVideoVolumeForFFMPEG(boomer)
        filter_params = filter_params + f"""        

{inp_v} split=2 
[fin1] [fin3];

[fin1] trim= end= {boomin_time_start}, setpts=PTS-STARTPTS
[botv];

[fin3] trim= start= {boomin_time_start}, setpts=PTS-STARTPTS
[uppv];

[{first_file_idx}] trim= end= {duration}, scale= w= {vid_width if vid_width else -1}:h= {vid_height if vid_height else -1}, setpts=PTS-STARTPTS
[b_video];

[uppv] [b_video] overlay= {posx}:{posy}:enable='between(t, 0, {duration})'
[uppv_mix];

{inp_a} asplit=2 
[fin2] [fin4];

[fin2] atrim= end= {boomin_time_start}, asetpts=PTS-STARTPTS
[bota];

[fin4] atrim= start= {boomin_time_start}, asetpts=PTS-STARTPTS
[uppa];

[{first_file_idx}] atrim= end= {duration}, volume= {volume}, asetpts=PTS-STARTPTS
[b_audio];

[uppa] [b_audio] amix= dropout_transition=0, dynaudnorm
[uppa_mix];
 
[botv] [bota] [uppv_mix] [uppa_mix] concat=n=2:v=1:a=1
"""

    tail = boomers[1:]
    for idx, boomer in enumerate(tail, first_file_idx + 1):
        vid_width = bu.getBoomerVideoWidthForFFMPEG(boomer, main_clip_width)
        vid_height = bu.getBoomerVideoHeightForFFMPEG(boomer, main_clip_height)     

        positionx = bu.getBoomerVideoPosXForFFMPEG(boomer)
        positiony = bu.getBoomerVideoPosYForFFMPEG(boomer)        

        if positionx == Position.get("TOP") :
            posx = "x=main_w-overlay_w-12"
        elif positionx == Position.get("CENTER") :
            posx = "x=main_w/2-overlay_w/2"
        elif positionx == Position.get("BOTTOM") :
            posx = "x=12"
        elif positionx == Position.get("RANDOM") :
            if main_clip_width and vid_width :
                randomx = random.choice(range(int(float(0.8 * main_clip_width - vid_width))))
            elif main_clip_width and vid_height :
                randomx = random.choice(range(int(float(0.8 * main_clip_width - vid_height))))
            else :
                randomx = 12
            for _ in range(8) :
                print(f"randomx: {randomx}, main_w: {main_clip_width}, img_w: {vid_width}", end="\n")
            posx = "x={}".format(randomx)            

        if positiony == Position.get("TOP") :
            posy = "y=12"
        elif positiony == Position.get("CENTER") :
            posy = "y=main_h/2-overlay_h/2"
        elif positiony == Position.get("BOTTOM") :
            posy = "y=main_h-overlay_h-12"
        elif positiony == Position.get("RANDOM") :
            if main_clip_height and vid_height :
                randomy = random.choice(range(main_clip_height - vid_height))
            else :
                randomy = 12
            for _ in range(8) :
                print(f"randomy: {randomy}, main_h: {main_clip_height}, img_h: {vid_height}", end="\n")
            posy = "y={}".format(randomy)            


        boomin_time_start = bu.getBoomerBoominTimeForFFMPEG(boomer)
        duration = bu.getBoomerVideoDurationForFFMPEG(boomer)
        volume = bu.getBoomerVideoVolumeForFFMPEG(boomer)        
        filter_params = filter_params + f"""{out_v}{out_a};

{out_v} split=2 
[fin1] [fin3];

[fin1] trim= end= {boomin_time_start}, setpts=PTS-STARTPTS
[botv];

[fin3] trim= start= {boomin_time_start}, setpts=PTS-STARTPTS
[uppv];

[{idx}] trim= end= {duration}, scale= w= {vid_width if vid_width else -1}:h= {vid_height if vid_height else -1}, setpts=PTS-STARTPTS
[b_video];

[uppv] [b_video] overlay= {posx}:{posy}:enable='between(t, 0, {duration})'
[uppv_mix];

{out_a} asplit=2 
[fin2] [fin4];

[fin2] atrim= end= {boomin_time_start}, asetpts=PTS-STARTPTS
[bota];

[fin4] atrim= start= {boomin_time_start}, asetpts=PTS-STARTPTS
[uppa];

[{idx}] atrim= end= {duration}, volume= {volume}, asetpts=PTS-STARTPTS
[b_audio];

[uppa] [b_audio] amix= dropout_transition=0, dynaudnorm
[uppa_mix];
 
[botv] [bota] [uppv_mix] [uppa_mix] concat=n=2:v=1:a=1
"""

    return filter_params





def buildVideoConcatFilterParams(boomers= [], inp_v= "[0]", inp_a= "[0]", out_v= "[outv]", out_a= "[outa]", first_file_idx= 0, main_clip_params= {}):
    filter_params = ""
    main_clip_width = main_clip_params.get("width") if main_clip_params.get("width") else 0
    main_clip_height = main_clip_params.get("height") if main_clip_params.get("height") else 0

    duration = 0

    head = boomers[:1]
    for boomer in head:
        boomin_time_start = bu.getBoomerBoominTimeForFFMPEG(boomer)
        duration = bu.getBoomerVideoDurationForFFMPEG(boomer)
        volume = bu.getBoomerVideoVolumeForFFMPEG(boomer)

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

        boomin_time_start = bu.getBoomerBoominTimeForFFMPEG(boomer)
        duration = bu.getBoomerVideoDurationForFFMPEG(boomer)
        volume = bu.getBoomerVideoVolumeForFFMPEG(boomer)

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
        boomin_time_start = bu.getBoomerBoominTimeForFFMPEG(boomer)
        duration = bu.getBoomerImageDurationForFFMPEG(boomer)

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

        boomin_time_start = bu.getBoomerBoominTimeForFFMPEG(boomer)
        duration = bu.getBoomerImageDurationForFFMPEG(boomer)

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



def download_clip_and_audio(from_= "./", to_v= "./", to_a= "./"):
    
    subprocess.run([
        variables.FFMPEG_PATH,
        "-y",
        "-i",
        from_,
        "-map",
        "0",
        '-c',
        "copy",
        to_v,
        "-map",
        "0:a",
        "-ac",
        "1",
        to_a
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


