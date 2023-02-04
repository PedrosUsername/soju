import os
import script

from moviepy.editor import *


# soju will need you to give the file path to it 
def getFile():
    return sys.argv[1] if len(sys.argv) > 1 else None



# soju may transcribe (t), detail (d), or look for a word (d [term]) in the audio file
def getAction():
    return sys.argv[2] if len(sys.argv) > 2 else None



# soju will look for this word in the audio file
def getTerm():
    return sys.argv[3] if len(sys.argv) > 3 else None



video_filename = getFile()
action = getAction()
term_to_find = getTerm()

if(video_filename is not None):
    audio_filename = video_filename + '.wav'

    clip = VideoFileClip(video_filename)

    clipAudio = clip.audio
    clipAudio.write_audiofile(audio_filename, ffmpeg_params=["-ac", "1"])

    list_of_words = script.main(audio_filename, action, term_to_find)
    os.remove(audio_filename)

    for word in list_of_words:
        print(word.to_string())

    if((list_of_words is not None) and (len(list_of_words) < 1)):
        print('no word was found')

else:
    print('video file not found')