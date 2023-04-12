import time
import ntpath
import json
import filetype
import tempfile

from moviepy.editor import *

from .settings import variables
from . import ffmpeg_utils, vosk_utils
from . import ImageMergeStrategy













def get_boomers(jsonfilepath):
    describe_json = []
    with open(jsonfilepath, 'r') as f:
        describe_json = f.read()

    return json.loads(describe_json)["boomers"]




def filterBoomers(og_clip_duration= 0, boomers= []):
    out_of_bounds_boomers_bot = []
    regular_boomers = []
    out_of_bounds_boomers_top = []

    for boomer in boomers:
        boomin_time = boomer["word"][get_boom_trigger(boomer)]
        if boomin_time > 0 and boomin_time < og_clip_duration:
            regular_boomers = regular_boomers + [boomer]
        elif boomin_time <= 0:
            out_of_bounds_boomers_bot = out_of_bounds_boomers_bot + [boomer]
        elif boomin_time >= og_clip_duration:
            out_of_bounds_boomers_top = out_of_bounds_boomers_top + [boomer]

    return (out_of_bounds_boomers_top, regular_boomers, out_of_bounds_boomers_bot)





def makeItGoofy(videofilepath="", jsonfilepath= None):
    time_start = time.time()

    og_clip = getClipWithMoviePy(videofilepath)
    boomers = get_boomers(jsonfilepath)

    boomers_top, boomers_mid, boomers_bot = filterBoomers(og_clip.duration, boomers)

    clip = videofilepath
    for boomer in boomers_mid:

        if boomer["image"] is not None and boomer["image"]["conf"] is not None:
            if boomer["image"]["conf"]["imageconcatstrategy"] == ImageMergeStrategy.FAST_COMPOSE_ENUM:
                ffmpeg_utils.quickOverlay(clip, boomer, "overlay.mp4", variables.DEFAULT_TMP_FILE_PATH)

                output_file = generate_output_file_name(videofilepath)
                
                if (boomer["audio"] is not None and boomer["audio"]["files"] is not None and len(boomer["audio"]["files"]) > 0):
                    ffmpeg_utils.slowAmix(variables.DEFAULT_TMP_FILE_PATH + "overlay.mp4", boomer, output_file)
                else:
                    ffmpeg_utils.copy(from_= variables.DEFAULT_TMP_FILE_PATH + "overlay.mp4", to_= output_file)

                clip = output_file

            elif boomer["image"]["conf"]["imageconcatstrategy"] == ImageMergeStrategy.COMPOSE_ENUM:
                ffmpeg_utils.splitClip(clip, boomer, variables.DEFAULT_TMP_FILE_PATH)
                editUpperHalfVideo(boomer, variables.DEFAULT_TMP_FILE_PATH)

                output_file = generate_output_file_name(videofilepath)
                
                ffmpeg_utils.concatClipHalves(output_file, variables.DEFAULT_TMP_FILE_PATH)
                clip = output_file


            elif boomer["image"]["conf"]["imageconcatstrategy"] == ImageMergeStrategy.CONCAT_ENUM:
                ffmpeg_utils.splitClip(clip, boomer, variables.DEFAULT_TMP_FILE_PATH)
                editUpperHalfVideo(boomer, variables.DEFAULT_TMP_FILE_PATH)

                clip_extend(boomers_mid, boomer["image"]["conf"]["max_duration"])
                output_file = generate_output_file_name(videofilepath)
                
                ffmpeg_utils.concatClipHalves(output_file, variables.DEFAULT_TMP_FILE_PATH)
                clip = output_file

    time_end = time.time() - time_start
    print("\n")
    print("it took {:.2f} seconds to make it goofy".format(time_end))




def editUpperHalfVideo(boomer= None, tmp_dir= ""):
    print("\n")
    print('Soju - Working on boomer [ "{}" ]'.format(boomer["word"]["content"]))
    print("""soju - Boomin' at second [ {:.2f} ]""".format(boomer["word"][get_boom_trigger(boomer)]))
    print("""soju - visual media [ {} ]""".format(boomer["image"]["file"]))
    print("""soju - audio media [ {} ]""".format(str(boomer["audio"]["files"])))
    print("\n")

    upper_half_file_tmp = "{}/upper_half_0.mp4".format(tmp_dir)
    upper_half_file_final = "{}/upper_half.mp4".format(tmp_dir)

    upper_half = get_and_prepare_clip_for_moviepy_edition(upper_half_file_tmp)
    media = reach_goofyahh_image(boomer)
    audioarray = boomer["audio"]["files"] if (boomer["audio"] is not None and boomer["audio"]["files"] is not None) else []

    upper_half = merge_image_video(
        media,
        upper_half,
        boomer
    )

    upper_half = merge_audioarray_video(
        audioarray,
        upper_half,
        boomer
    )

    upper_half.write_videofile(
        upper_half_file_final,
        fps= 30,
        threads= 4,
        logger= "bar",
        ffmpeg_params= ["-s", "1280x720"]
    )

def buildvisuals(boomers= None, tmp_dir= ""):

    for counter, boomer in enumerate(boomers, 1):
        clip = get_and_prepare_clip_for_moviepy_edition("{}/clip_piece_{}.mp4".format(tmp_dir, counter))

        boomin_time = boomer["word"][get_boom_trigger(boomer)]
        image = reach_goofyahh_image(boomer)
        audioarray = boomer["audio"]["files"] if (boomer["audio"] is not None and boomer["audio"]["files"] is not None) else []

        print("\n")
        print('Soju - Working on boomer [ "{}" ]'.format(boomer["word"]["content"]))
        print("""soju - Boomin' at second [ {:.2f} ]""".format(boomin_time))
        print("""soju - visual media [ {} ]""".format(boomer["image"]["file"]))
        print("""soju - audio media [ {} ]""".format(str(audioarray)))
        print("\n")

        clip = merge_image_video(
            image,
            clip,
            boomer
        )

        clip.write_videofile(
            "{0}/v_clip_piece_{1}.mp4".format(".", counter),
            fps= 30,
            threads= 4,
            logger= "bar"
        )


def buildSojuFile(videofilepath= None, jsonfilepath= None):
    if(videofilepath is not None and jsonfilepath is None):
        with tempfile.TemporaryDirectory() as tmp_dir:
            clip = VideoFileClip(videofilepath)
            clip.audio.write_audiofile(tmp_dir + "/" + variables.TMP_AUDIO_FILE_NAME, ffmpeg_params=["-ac", "1"])

            print("Soju - clip duration: {}".format(clip.duration))

            list_of_words = vosk_utils.voskDescribe(tmp_dir + "/" + variables.TMP_AUDIO_FILE_NAME)

        with open(generate_soju_file_name(videofilepath), 'w') as f:
            f.writelines('{\n\t"data": [' + '\n')
            for i, word in enumerate(list_of_words):
                comma = ',' if i < (len(list_of_words) - 1) else ''
                f.writelines('\t\t{0}{1}\n'.format(word.to_string(), comma))
            f.writelines('\t],\n\n')
            f.writelines('\t"boomers": [\n\n\t]\n}')
        
        clip.close()
        return None







def getNullBoomer():
    return {
            "word": None,
            "image": {
                "file": None,
                "conf": {
                    "boom_trigger": variables.DEFAULT_BOOM_TRIGGER,
                    "height": variables.DEFAULT_IMAGE_RESOLUTION_HEIGHT,
                    "width": variables.DEFAULT_IMAGE_RESOLUTION_WIDTH,
                    "position": {
                        "x": variables.DEFAULT_IMAGE_POSITION_X,
                        "y": variables.DEFAULT_IMAGE_POSITION_Y
                    },
                    "imageconcatstrategy": variables.DEFAULT_IMAGE_CONCAT_STRATEGY,
                    "max_duration": variables.MAX_IMAGE_DURATION,
                    "volume": variables.DEFAULT_IMAGE_VOLUME
                }
            },
            "audio": {
				"files": [],
				"conf": {
					"max_duration": variables.MAX_AUDIO_DURATION,
					"volume": variables.DEFAULT_SOUND_VOLUME
				}
			}
        }





def isVideo(our_file):
    kind = filetype.guess(our_file)
    if kind is None:
        print('Cannot guess file type!')
        return False
    
    if kind.extension != "ogv" and kind.extension != "mp4" and kind.extension != "mpeg" and kind.extension != "avi" and kind.extension != "mov":
        return False
    else:
        return True

























def get_base_file_name_from(videofilepath):
    filename = ntpath.basename(videofilepath)
    head, tail = filename[::-1].split(".", 1)
    return tail[::-1]





def generate_soju_file_name(videofilepath):
    videofilename = get_base_file_name_from(videofilepath)
    return "{}{}.soju.json".format(variables.PATH_DEFAULT_JSON_FILE, videofilename)





def generate_output_file_name(videofilepath):
    videofilename = get_base_file_name_from(videofilepath)
    return "{}{}.mp4".format(variables.DEFAULT_OUTPUT_PATH, videofilename)





def reach_goofyahh_image(boomer= getNullBoomer()):
    duration = boomer["image"]["conf"]["max_duration"]
    height = boomer["image"]["conf"]["height"]
    width = boomer["image"]["conf"]["width"]
    volume = boomer["image"]["conf"]["volume"]
    position = (boomer["image"]["conf"]["position"]["x"], boomer["image"]["conf"]["position"]["y"])
    goofy_image = '{0}{1}'.format(variables.DEFAULT_IMAGE_PATH, boomer["image"]["file"]) if (boomer["image"] is not None and boomer["image"]["file"] is not None) else variables.DEFAULT_NULL_IMAGE_FILE
    visual = None

    if(isVideo(goofy_image)):
        visual = VideoFileClip(goofy_image)
        visual.audio = visual.audio.volumex(volume)
        visual = CompositeVideoClip([visual, reach_goofyahh_image().subclip(0, duration)])
        visual = visual.subclip(0, duration)
    else:
        visual = ImageClip(goofy_image).subclip(0, duration)

    if(width is None or height is None):
        return visual.set_pos(position, relative= True)
    else:
        return visual.set_pos(position, relative= True).resize((width, height))





def reach_goofyahh_audio(filename):
    goofy_audio = '{0}{1}'.format(variables.DEFAULT_AUDIO_PATH, filename) if filename is not None else variables.DEFAULT_NULL_AUDIO_FILE
    audio = AudioFileClip(goofy_audio)
    # return audio                                             # no audio fadeout ?
    return audio.fx(afx.audio_fadeout, audio.duration * (2/3)) # yes audio fadeout ?





def clip_extend(boomers, extra= variables.MAX_IMAGE_DURATION):
    for boomer in boomers:
        boomer["word"]["start"] = boomer["word"]["start"] + extra
        boomer["word"]["end"] = boomer["word"]["end"] + extra





def merge_image_video(image, video, boomer):
    if boomer["image"] is not None and boomer["image"]["conf"] is not None and boomer["image"]["conf"]["imageconcatstrategy"] == ImageMergeStrategy.CONCAT_ENUM:
        result = CompositeVideoClip([video.set_start(boomer["image"]["conf"]["max_duration"]), image])
    else:
        result = CompositeVideoClip([video, image.crossfadeout(.5)])

    return result





def merge_audio_video(video, audio):
    if video.audio is None:
        null_audio = reach_goofyahh_audio(None)
        video.audio = null_audio
    return CompositeAudioClip([video.audio, audio])





def merge_audioarray_video(audioarray, video, boomer):
    for audio in audioarray:
        edit = reach_goofyahh_audio(audio)
        duration = boomer["audio"]["conf"]["max_duration"] if boomer["audio"]["conf"]["max_duration"] is not None else variables.MAX_AUDIO_DURATION
        volume = boomer["audio"]["conf"]["volume"] if boomer["audio"]["conf"]["volume"] is not None else variables.DEFAULT_VOLUME
        edit = edit.subclip(0, duration) if edit.duration > duration else edit.subclip(0, edit.end)
        edit = edit.volumex(volume)

        video.audio = merge_audio_video(
            video,
            edit
        )

    return video






def get_and_prepare_clip_for_vosk_description(videofilepath):
    result = VideoFileClip(videofilepath)
    result.audio.write_audiofile(variables.TMP_PATH + variables.TMP_AUDIO_FILE_NAME, ffmpeg_params=["-ac", "1"])
    return result





def get_and_prepare_clip_for_moviepy_edition(videofilepath, audio= True):
    return VideoFileClip(
        videofilepath,
        target_resolution=(variables.OUTPUT_RESOLUTION_HEIGHT, variables.OUTPUT_RESOLUTION_WIDTH),
        audio= audio
    )




def getClipWithMoviePy(videofilepath, audio= True):
    return VideoFileClip(
        videofilepath,
        audio= audio
    )






def get_boom_trigger(boomer= None):
    if boomer is None:
        return variables.DEFAULT_BOOM_TRIGGER if variables.DEFAULT_BOOM_TRIGGER is not None else "end"
    else:
        return boomer["image"]["conf"]["boom_trigger"]








