import ntpath
import random
import json
import wave
import os

from vosk import Model, KaldiRecognizer
from moviepy.editor import *
from itertools import cycle

from .settings import variables
from . import Word as custom_word
from . import ImageMergeStrategy















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

    obj["image"] = image_name
    obj["audio"] = variables.DEFAULT_AUDIO_FILE + [next(audio_names) for i in range(variables.CHOOSE_AUDIO_AT_RANDOM)]
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





def get_goofy_image(word):
    goofy_image = '{0}{1}'.format(variables.DEFAULT_IMAGE_PATH, word["image"]) if word["image"] is not None else variables.DEFAULT_NULL_IMAGE_FILE
    image = ImageClip(goofy_image, duration= variables.MAX_IMAGE_DURATION)
    return image.subclip(0, image.end).set_pos(("center","center")).resize((1920, 1080)).crossfadeout(.5)





def get_goofy_audio(element):
    goofy_audio = '{0}{1}'.format(variables.DEFAULT_AUDIO_PATH, element) if element is not None else variables.DEFAULT_NULL_AUDIO_FILE
    audio = AudioFileClip(goofy_audio)
    audio = audio.subclip(0, variables.MAX_AUDIO_DURATION) if audio.duration > variables.MAX_AUDIO_DURATION else audio.subclip(0, audio.end)
    return audio.fx(afx.audio_fadeout, audio.duration * (2/3))





def clip_extend(goofy_words):
    for word in goofy_words:
        word["start"] = word["start"] + variables.MAX_IMAGE_DURATION
        word["end"] = word["end"] + variables.MAX_IMAGE_DURATION





def merge_visuals(upper_half, image, word, goofy_words):
    if word["imageconcatstrategy"] == ImageMergeStrategy.CONCAT_ENUM:
        result = concatenate_videoclips([image, upper_half])
        clip_extend(goofy_words)
    else:
        result = CompositeVideoClip([upper_half, image])
    return result





def merge_sounds(upper_half, audio):
    return CompositeAudioClip([upper_half.audio, audio])





def get_and_prepare_clip_for_vosk_description(videofilepath):
    result = VideoFileClip(videofilepath, target_resolution=(1080, 1920))
    result.audio.write_audiofile(variables.PATH_TMP_AUDIO, ffmpeg_params=["-ac", "1"])
    return result





def get_and_prepare_clip_for_moviepy_edition(videofilepath):
    return VideoFileClip(videofilepath, target_resolution=(1080, 1920))





def final_merge(bottom_half, uppper_half):
    return concatenate_videoclips([bottom_half, uppper_half])





def get_trigger_settings():
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
            obj["imageconcatstrategy"] = ImageMergeStrategy.COMPOSE_ENUM
            new_word = constructWord(obj, image_files)
            if new_word.image is not None and variables.ALLOW_IMAGE_REPETITION_WHEN_RANDOM is not True:                                
                image_files.remove(new_word.image)
            word_list.append(new_word)  # and add it to list
    wf.close()  # close audiofile
    os.remove(variables.PATH_TMP_AUDIO)
    return word_list

