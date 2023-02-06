import json
import wave

from vosk import Model, KaldiRecognizer

from . import Word as custom_word
from .settings import variables






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
            obj["image"] = variables.DEFAULT_IMAGE_FILE
            obj["audio"] = [variables.DEFAULT_AUDIO_FILE]
            w = custom_word.Word(obj)  # create custom Word object
            wordList.append(w)  # and add it to list
    wf.close()  # close audiofile

    return wordList

