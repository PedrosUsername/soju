import json
import wave
import Word as custom_word
import speech_recognition as sr

from vosk import Model, KaldiRecognizer







# get just the text
def voskTranscribe(fil, mod):
    r = sr.Recognizer()
    with sr.AudioFile(fil) as source:
        audio = r.record(source)

    try:
        model = Model(mod)
        rec = KaldiRecognizer(model, 16000)
        rec.AcceptWaveform(audio.get_raw_data(convert_rate=16000, convert_width=2))
        return rec.FinalResult()
    except sr.UnknownValueError:
        raise Exception("Vosk could not understand audio")
    except sr.RequestError as e:
        raise Exception("Could not request results from Vosk; {0}".format(e))



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
            w = custom_word.Word(obj)  # create custom Word object
            wordList.append(w)  # and add it to list
    wf.close()  # close audiofile

    return wordList

