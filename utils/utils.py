import ntpath
import random
import json
import wave
import os

from vosk import Model, KaldiRecognizer
from itertools import cycle

from . import Word as custom_word
from . import ImageMergeStrategy
from .settings import variables









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







def voskDescribe(fil, mod):
    image_files = os.listdir(variables.DEFAULT_IMAGE_PATH)
    model = Model(mod)
    wf = wave.open(fil, "rb")
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

    return word_list

