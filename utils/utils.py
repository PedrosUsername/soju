import random
import json
import wave
import os

from vosk import Model, KaldiRecognizer
from itertools import cycle

from . import Word as custom_word
from .settings import variables









def file_is_a_good_choice(image_file):
    return os.path.isfile('{0}{1}'.format(variables.DEFAULT_IMAGE_PATH, image_file)) and image_file not in variables.IGNORE_IMAGE_FILE_LIST




def getRandomizedImageFileName():
    image_files = os.listdir(variables.DEFAULT_IMAGE_PATH)

    flag = False
    while flag is False:
        image_file = random.choice(image_files)
        flag = True if file_is_a_good_choice(image_file) else False

    return image_file



def getRandomizedAudioFileNames():
    audio_files = os.listdir(variables.DEFAULT_AUDIO_PATH)
    random.shuffle(audio_files)
    return [aud for aud in audio_files if os.path.isfile('{0}{1}'.format(variables.DEFAULT_AUDIO_PATH, aud)) and aud not in variables.IGNORE_AUDIO_FILE_LIST and aud not in variables.DEFAULT_AUDIO_FILE]



def constructWord(obj):
    image_name = getRandomizedImageFileName() if variables.CHOOSE_IMAGE_AT_RANDOM == True else variables.DEFAULT_IMAGE_FILE
    audio_names = cycle(getRandomizedAudioFileNames())

    obj["image"] = image_name
    obj["audio"] = variables.DEFAULT_AUDIO_FILE + [next(audio_names) for i in range(variables.CHOOSE_AUDIO_AT_RANDOM)]
    return custom_word.Word(obj)  # create custom Word object










def voskDescribe(fil, mod):
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
            word_list.append(constructWord(obj))  # and add it to list
    wf.close()  # close audiofile

    return word_list

