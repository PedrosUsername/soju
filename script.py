import filetype
import json
import sys
import wave
import Word as custom_word
import speech_recognition as sr

from pydub import AudioSegment
from vosk import Model, KaldiRecognizer, SetLogLevel



def convertMp3ToWav(f):
    song = AudioSegment.from_file(f, format='mp3')
    return song.export(format='wav')



# validate file type
def validateFile(f):
    try:
        ourBestGess = filetype.guess(f)

        if ourBestGess is None:
            raise Exception('unsupported file type')
        elif (ourBestGess.extension == 'wav'):
            return f
        elif (ourBestGess.extension == 'mp3'):
            return convertMp3ToWav(f)
        else:
            raise Exception('unsupported file type')
    except FileNotFoundError:
        raise Exception('File not found')



# get file
def getFile():
    rawFile = sys.argv[1] if len(sys.argv) > 1 else None
    return validateFile(rawFile)



# get file
def getAction():
    return sys.argv[2] if len(sys.argv) > 2 else None



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



def voskDetail(fil, mod):
    model = Model(mod)
    wf = wave.open(fil, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    # get the list of JSON dictionaries
    results = []
    # recognize speech using vosk model
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











model_path = "model"
audio_filename = getFile()

action = getAction()
if (action == 'transcribe' or action == 't'):
    print(voskTranscribe(audio_filename, model_path))
elif (action == 'detail' or action == 'd'):
    list_of_words = voskDetail(audio_filename, model_path)
    for word in list_of_words:
        print(word.to_string())
else:
    print('no action selected')
