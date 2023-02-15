import ntpath
import random
import json
import wave
import os
import filetype

from vosk import Model, KaldiRecognizer
from moviepy.editor import *
from itertools import cycle

from .settings import variables
from . import Word as custom_word
from . import ImageMergeStrategy














def getNullBoomer():
    return {
            "image": {
                "file": None,
                "conf": {
                    "height": variables.DEFAULT_IMAGE_RESOLUTION_HEIGHT,
                    "width": variables.DEFAULT_IMAGE_RESOLUTION_WIDTH,
                    "imageconcatstrategy": variables.DEFAULT_IMAGE_CONCAT_STRATEGY,
                    "max_duration": variables.MAX_IMAGE_DURATION,
                    "animation": None
                }
            },
            "audio": {
				"files": [],
				"conf": {
					"max_duration": variables.MAX_AUDIO_DURATION,
					"volume": variables.DEFAULT_VOLUME
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





def constructWord(obj, image_files):
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
            "height": variables.DEFAULT_IMAGE_RESOLUTION_HEIGHT,
            "width": variables.DEFAULT_IMAGE_RESOLUTION_WIDTH,
            "imageconcatstrategy": variables.DEFAULT_IMAGE_CONCAT_STRATEGY,
            "max_duration": variables.MAX_IMAGE_DURATION,
            "animation": None
        }
    }

    obj["audio"] = {
        "files": variables.DEFAULT_AUDIO_FILE + [next(audio_names) for i in range(variables.CHOOSE_AUDIO_AT_RANDOM)],
        "conf": {
            "max_duration": variables.MAX_AUDIO_DURATION,
            "volume": 1
        }
    }

    return custom_word.Word(obj)  # create custom Word object





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
    goofy_image = '{0}{1}'.format(variables.DEFAULT_IMAGE_PATH, boomer["image"]["file"]) if (boomer["image"] is not None and boomer["image"]["file"] is not None) else variables.DEFAULT_NULL_IMAGE_FILE
    visual = None

    if(isVideo(goofy_image)):
        visual = VideoFileClip(goofy_image)
        visual = CompositeVideoClip([visual, reach_goofyahh_image().subclip(0, duration)])
        visual = visual.subclip(0, duration)
    else:
        visual = ImageClip(goofy_image).subclip(0, duration)
    return visual.set_pos(("center","center")).resize((width, height))





def reach_goofyahh_audio(filename):
    goofy_audio = '{0}{1}'.format(variables.DEFAULT_AUDIO_PATH, filename) if filename is not None else variables.DEFAULT_NULL_AUDIO_FILE
    audio = AudioFileClip(goofy_audio)
    return audio.fx(afx.audio_fadeout, audio.duration * (2/3))





def clip_extend(boomers, extra= variables.MAX_IMAGE_DURATION):
    for boomer in boomers:
        boomer["word"]["start"] = boomer["word"]["start"] + extra
        boomer["word"]["end"] = boomer["word"]["end"] + extra





def merge_image_video(image, video, boomer, boomers):
    if boomer["image"] is not None and boomer["image"]["conf"] is not None and boomer["image"]["conf"]["imageconcatstrategy"] == ImageMergeStrategy.CONCAT_ENUM:
        result = CompositeVideoClip([video.set_start(boomer["image"]["conf"]["max_duration"]), image])
        clip_extend(boomers, boomer["image"]["conf"]["max_duration"])
    else:
        result = CompositeVideoClip([video.set_start(0), image.crossfadeout(.5)])

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
    result.audio.write_audiofile(variables.PATH_TMP_AUDIO, ffmpeg_params=["-ac", "1"])
    return result





def get_and_prepare_clip_for_moviepy_edition(videofilepath):
    return VideoFileClip(videofilepath, target_resolution=(variables.OUTPUT_RESOLUTION_HEIGHT, variables.OUTPUT_RESOLUTION_WIDTH))





def final_merge(bottom_half, uppper_half):
    return concatenate_videoclips([bottom_half, uppper_half])





def get_boom_trigger():
    return "end" if variables.BOOM_AT_WORD_END else "start"





def voskDescribe():
    image_files = os.listdir(variables.DEFAULT_IMAGE_PATH)
    model = Model(variables.PATH_MODEL)
    wf = wave.open(variables.PATH_TMP_AUDIO, "rb")
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
            new_word = constructWord(obj, image_files)
            if new_word.image is not None and new_word.image["file"] is not None and variables.ALLOW_IMAGE_REPETITION is not True and variables.CHOOSE_IMAGE_AT_RANDOM > 0:
                image_files.remove(new_word.image["file"])
            word_list.append(new_word)  # and add it to list
    wf.close()  # close audiofile
    os.remove(variables.PATH_TMP_AUDIO)
    return word_list

