import ntpath
import random
import json
import wave
import os
import filetype
import tempfile

from vosk import Model, KaldiRecognizer
from moviepy.editor import *
from itertools import cycle

from .settings import variables
from . import ffmpeg_utils
from . import Boomer as custom_b
from . import ImageMergeStrategy













def get_boomers(jsonfilepath):
    describe_json = []
    with open(jsonfilepath, 'r') as f:
        describe_json = f.read()

    return json.loads(describe_json)["boomers"]



def makeItGoofy(videofilepath="", jsonfilepath= None):
    with tempfile.TemporaryDirectory() as tmp_dir:
        ffmpeg_utils.splitClip(videofilepath, jsonfilepath, tmp_dir + "/")
        goofy_edit = edit(videofilepath, jsonfilepath, tmp_dir + "/")
    return goofy_edit


def edit(videofilepath="", jsonfilepath= None, tmp_dir= ""):
    if(jsonfilepath is not None):
        boomers = get_boomers(jsonfilepath)

        og_clip = get_and_prepare_clip_for_moviepy_edition(videofilepath)

        clip_pieces_top = []
        clip_pieces_mid = ["clip_piece_0.mp4"]
        clip_pieces_bot = []

        for counter, boomer in enumerate(boomers, 1):
            boomin_time = boomer["word"][get_boom_trigger(boomer)]
            if boomin_time > 0 and boomin_time < og_clip.duration:
                clip_pieces_mid = clip_pieces_mid + ["clip_piece_{}.mp4".format(counter)]
            elif boomin_time <= 0:
                clip_pieces_bot = clip_pieces_bot + ["clip_piece_{}.mp4".format(counter)]
            elif boomin_time >= og_clip.duration:
                clip_pieces_top = clip_pieces_top + ["clip_piece_{}.mp4".format(counter)]

        full_clip = [get_and_prepare_clip_for_moviepy_edition("{}/{}".format(tmp_dir, clip_pieces_mid[0]))]
        for counter, boomer in enumerate(boomers, 1):
            clip = get_and_prepare_clip_for_moviepy_edition("{}/{}".format(tmp_dir, clip_pieces_mid[counter]))

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
                boomer,
            )

            clip = merge_audioarray_video(
                audioarray,
                clip,
                boomer
            )

            full_clip = full_clip + [clip]

        return concatenate_videoclips(full_clip)



def soju(videofilepath= None, jsonfilepath= None):
    if(videofilepath is not None and jsonfilepath is None):
        with tempfile.TemporaryDirectory() as tmp_dir:
            clip = VideoFileClip(videofilepath)
            clip.audio.write_audiofile(tmp_dir + "/" + variables.TMP_AUDIO_FILE_NAME, ffmpeg_params=["-ac", "1"])

            print("Soju - clip duration: {}".format(clip.duration))

            list_of_words = voskDescribe(tmp_dir + "/" + variables.TMP_AUDIO_FILE_NAME)

        with open(generate_soju_file_name(videofilepath), 'w') as f:
            f.writelines('{\n\t"data": [' + '\n')
            for i, word in enumerate(list_of_words):
                comma = ',' if i < (len(list_of_words) - 1) else ''
                f.writelines('\t\t{0}{1}\n'.format(word.to_string(), comma))
            f.writelines('\t],\n\n')
            f.writelines('\t"boomers": [\n\n\t]\n}')
        
        clip.close()
        return None




    elif(videofilepath is not None and jsonfilepath is not None):
        boomers = get_boomers(jsonfilepath)

        clip = get_and_prepare_clip_for_moviepy_edition(videofilepath)

        for boomer in boomers:
            boom_trigger = get_boom_trigger(boomer)
            image = reach_goofyahh_image(boomer)
            audioarray = boomer["audio"]["files"] if (boomer["audio"] is not None and boomer["audio"]["files"] is not None) else []

            print("\n")
            print('Soju - Working on boomer [ "{}" ]'.format(boomer["word"]["content"]))
            print("""soju - Boomin' at second [ {:.2f} ]""".format(boomer["word"][boom_trigger]))
            print("""soju - visual media [ {} ]""".format(boomer["image"]["file"]))
            print("""soju - audio media [ {} ]""".format(str(audioarray)))
            print("\n")

            if boomer["word"]["end"] > clip.start and boomer["word"]["start"] < clip.end:
                uppper_half = clip.subclip(boomer["word"][boom_trigger], clip.end)
                bottom_half = clip.subclip(clip.start, boomer["word"][boom_trigger])

                uppper_half = merge_image_video(
                    image,
                    uppper_half,
                    boomer,
                    boomers
                )

                uppper_half = merge_audioarray_video(
                    audioarray,
                    uppper_half,
                    boomer
                )
                clip = final_merge(bottom_half, uppper_half)
                
            elif boomer["word"]["end"] <= clip.start:
                uppper_half = clip.subclip(clip.start, clip.end)
                bottom_half = image

                bottom_half = merge_audioarray_video(
                    audioarray,
                    bottom_half,
                    boomer
                )

                clip_extend(boomers, boomer["image"]["conf"]["max_duration"])

                clip = final_merge(bottom_half, uppper_half)

            elif boomer["word"]["start"] >= clip.end:
                uppper_half = image
                bottom_half = clip.subclip(clip.start, clip.end)

                boomer["image"]["conf"]["imageconcatstrategy"] = ImageMergeStrategy.CONCAT_ENUM

                uppper_half = merge_audioarray_video(
                    audioarray,
                    uppper_half,
                    boomer
                )

                clip = final_merge(bottom_half, uppper_half)

        print("\nSoju - final clip duration in seconds: {:.2f}\n".format(clip.duration))
        return clip




def compose_them_clips(clip_array, enforce_resolution= False):
    aux_file_name = variables.TMP_PATH + variables.TMP_COMPOSE_FILE_NAME
    try:
        os.remove(aux_file_name) # this file is frick'n cursed
    except:
        print("ok")

    if enforce_resolution:
        composed_clips = CompositeVideoClip(
            clip_array,
            size= (
                variables.OUTPUT_RESOLUTION_WIDTH,
                variables.OUTPUT_RESOLUTION_HEIGHT
            )
        )
    else:
        composed_clips = CompositeVideoClip(clip_array)
    
    composed_clips.write_videofile(
        aux_file_name,
        fps= 30
    )

    clip = get_and_prepare_clip_for_moviepy_edition(aux_file_name)
    return clip





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





def file_is_a_good_choice(image_file):
    return os.path.isfile('{0}{1}'.format(variables.DEFAULT_IMAGE_PATH, image_file)) and image_file not in variables.IGNORE_IMAGE_FILE_LIST





def getRandomizedImageFileName(image_files):
    flag = False

    while flag is False:
        try:
            image_file = random.choice(image_files)
            flag = True if file_is_a_good_choice(image_file) else False
        except:
            image_file = None
            flag = True
    return image_file





def getRandomizedAudioFileNames():
    audio_files = os.listdir(variables.DEFAULT_AUDIO_PATH)
    random.shuffle(audio_files)
    return [aud for aud in audio_files if os.path.isfile('{0}{1}'.format(variables.DEFAULT_AUDIO_PATH, aud)) and aud not in variables.IGNORE_AUDIO_FILE_LIST and aud not in variables.DEFAULT_AUDIO_FILE]





def constructBoomer(obj, image_files):
    image_name = getRandomizedImageFileName(image_files) if variables.CHOOSE_IMAGE_AT_RANDOM == True else variables.DEFAULT_IMAGE_FILE
    audio_names = cycle(getRandomizedAudioFileNames())

    obj["word"] = {
        "content": obj["word"],
        "start": obj["start"],
        "end": obj["end"]
    }

    obj["image"] = {
        "file": image_name,
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
    }

    obj["audio"] = {
        "files": variables.DEFAULT_AUDIO_FILE + [next(audio_names) for i in range(variables.CHOOSE_AUDIO_AT_RANDOM)],
        "conf": {
            "max_duration": variables.MAX_AUDIO_DURATION,
            "volume": variables.DEFAULT_SOUND_VOLUME
        }
    }

    return custom_b.Boomer(obj)





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





def get_and_prepare_clip_for_moviepy_edition(videofilepath):
    return VideoFileClip(videofilepath, target_resolution=(variables.OUTPUT_RESOLUTION_HEIGHT, variables.OUTPUT_RESOLUTION_WIDTH))







def final_merge(bottom_half, uppper_half):

    return compose_them_clips(
        [
            bottom_half, 
            uppper_half.set_start(bottom_half.end)
        ],
        enforce_resolution= True
    )





def get_boom_trigger(boomer= None):
    if boomer is None:
        return variables.DEFAULT_BOOM_TRIGGER if variables.DEFAULT_BOOM_TRIGGER is not None else "end"
    else:
        return boomer["image"]["conf"]["boom_trigger"]







def voskDescribe(audio_file_path= ""):
    image_files = os.listdir(variables.DEFAULT_IMAGE_PATH)
    model = Model(variables.PATH_MODEL)
    wf = wave.open(audio_file_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    # recognize speech using vosk model
    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)
    part_result = json.loads(rec.FinalResult())
    results.append(part_result)

    # convert list of JSON dictionaries to list of 'Word' objects
    word_list = []
    for sentence in results:
        if len(sentence) == 1:
            # sometimes there are bugs in recognition
            # and it returns an empty dictionary
            # {'text': ''}
            continue
        for obj in sentence['result']:
            new_word = constructBoomer(obj, image_files)
            if new_word.image is not None and new_word.image["file"] is not None and variables.ALLOW_IMAGE_REPETITION is not True and variables.CHOOSE_IMAGE_AT_RANDOM > 0:
                image_files.remove(new_word.image["file"])
            word_list.append(new_word)  # and add it to list
    wf.close()  # close audiofile
    return word_list

