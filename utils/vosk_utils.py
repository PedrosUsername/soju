import random
import wave
import json
import os

from vosk import Model, KaldiRecognizer
from itertools import cycle

from . import Boomer as custom_b
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
