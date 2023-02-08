import random
import json
import wave
import os

from vosk import Model, KaldiRecognizer
from itertools import cycle

from . import Word as custom_word
from .settings import variables






def getRandomizedImageFileNames():
    image_files = os.listdir(variables.DEFAULT_IMAGE_PATH)
    random.shuffle(image_files)
    return [img for img in image_files if os.path.isfile('{0}{1}'.format(variables.DEFAULT_IMAGE_PATH, img)) and img not in variables.IGNORE_IMAGE_FILE_LIST]



def getRandomizedAudioFileNames():
    audio_files = os.listdir(variables.DEFAULT_AUDIO_PATH)
    random.shuffle(audio_files)
    return [aud for aud in audio_files if os.path.isfile('{0}{1}'.format(variables.DEFAULT_AUDIO_PATH, aud)) and aud not in variables.IGNORE_AUDIO_FILE_LIST and aud not in variables.DEFAULT_AUDIO_FILE]



def constructWord(obj):
    image_names = cycle([variables.DEFAULT_IMAGE_FILE] if variables.CHOOSE_IMAGE_AT_RANDOM is True else getRandomizedImageFileNames())
    audio_names = cycle(getRandomizedAudioFileNames())

    obj["image"] = next(image_names)
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
            partResult = json.loads(rec.Result())
            results.append(partResult)
    partResult = json.loads(rec.FinalResult())
    results.append(partResult)

    # convert list of JSON dictionaries to list of 'Word' objects
    wordList = []
    for sentence in results:
        if len(sentence) == 1:
            # sometimes there are bugs in recognition
            # and it returns an empty dictionary
            # {'text': ''}
            continue
        for obj in sentence['result']:
            wordList.append(constructWord(obj))  # and add it to list
    wf.close()  # close audiofile

    return wordList

