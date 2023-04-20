import random
import wave
import json
import os

from vosk import Model, KaldiRecognizer

from . import Boomer as custom_b
from .settings import variables





def image_file_is_a_good_choice(image_file= ""):
    return os.path.isfile('{0}{1}'.format(variables.DEFAULT_IMAGE_FOLDER, image_file)) and image_file not in variables.IGNORE_IMAGE_FILE_LIST

def audio_file_is_a_good_choice(audio_file= ""):
    return os.path.isfile('{0}{1}'.format(variables.DEFAULT_AUDIO_FOLDER, audio_file)) and audio_file not in variables.IGNORE_AUDIO_FILE_LIST

def video_file_is_a_good_choice(video_file= ""):
    return os.path.isfile('{0}{1}'.format(variables.DEFAULT_VIDEO_FOLDER, video_file)) and video_file not in variables.IGNORE_VIDEO_FILE_LIST

def getFile(files= []):
    if len(files) > 0:
        return random.choice(files)
    
    else:
        return None









def buildBoomer(obj, image_files, audio_files, video_files):
    image_file = getFile(image_files)
    audio_file = getFile(audio_files)
    video_file = getFile(video_files)

    obj["word"] = {
        "content": obj["word"],
        "start": obj["start"],
        "end": obj["end"],
        "trigger": variables.DEFAULT_BOOM_TRIGGER
    }

    obj["image"] = {
        "file": image_file,
        "conf": {
            "height": variables.DEFAULT_IMAGE_RESOLUTION_HEIGHT,
            "width": variables.DEFAULT_IMAGE_RESOLUTION_WIDTH,
            "mergestrategy": variables.DEFAULT_IMAGE_CONCAT_STRATEGY,
            "duration": variables.MAX_IMAGE_DURATION,
        }
    }    

    obj["audio"] = {
        "file": audio_file,
        "conf": {
            "duration": variables.MAX_AUDIO_DURATION,
            "volume": variables.DEFAULT_AUDIO_VOLUME
        }
    }

    obj["video"] = {
        "file": video_file,
        "conf": {
            "height": variables.DEFAULT_VIDEO_RESOLUTION_HEIGHT,
            "width": variables.DEFAULT_VIDEO_RESOLUTION_WIDTH,
            "mergestrategy": variables.DEFAULT_VIDEO_MERGE_STRATEGY,
            "duration": variables.MAX_VIDEO_DURATION,
            "volume": variables.DEFAULT_VIDEO_VOLUME,
        }
    }

    return custom_b.Boomer(obj)







def getValidImageFiles():
    image_files = os.listdir(variables.DEFAULT_IMAGE_FOLDER)

    if variables.DEFAULT_IMAGE_FILE != None:
        return [variables.DEFAULT_IMAGE_FILE]
    else:
        return [file for file in image_files if image_file_is_a_good_choice(file)]


def getValidAudioFiles():
    audio_files = os.listdir(variables.DEFAULT_AUDIO_FOLDER)

    if variables.DEFAULT_AUDIO_FILE != None:
        return [variables.DEFAULT_AUDIO_FILE]        
    else:
        return [file for file in audio_files if audio_file_is_a_good_choice(file)]    
    

def getValidVideoFiles():
    video_files = os.listdir(variables.DEFAULT_VIDEO_FOLDER)

    if variables.DEFAULT_VIDEO_FILE != None:
        return [variables.DEFAULT_VIDEO_FILE]
    else:
        return [file for file in video_files if video_file_is_a_good_choice(file)]












def voskDescribe(audio_file_path= ""):
    valid_image_files = getValidImageFiles()
    valid_audio_files = getValidAudioFiles()
    valid_video_files = getValidVideoFiles()

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
            new_word = buildBoomer(obj, valid_image_files, valid_audio_files, valid_video_files)

            if variables.ALLOW_IMAGE_REPETITION is False and new_word.image["file"] in valid_image_files:
                valid_image_files.remove(new_word.image["file"])

            if variables.ALLOW_AUDIO_REPETITION is False and new_word.audio["file"] in valid_audio_files:
                valid_audio_files.remove(new_word.audio["file"])

            if variables.ALLOW_VIDEO_REPETITION is False and new_word.video["file"] in valid_video_files:
                valid_video_files.remove(new_word.video["file"])

            word_list.append(new_word)  # and add it to list

    wf.close()  # close audiofile
    return word_list
