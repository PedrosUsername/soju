import os
import script

from moviepy.editor import *



ASSETS_PATH = "./assets"

# soju will need you to give the file path to it 
def getFile():
    return "{0}/video/{1}".format(ASSETS_PATH, sys.argv[1]) if len(sys.argv) > 1 else None



# soju may transcribe (t), detail (d), or look for a word (d [term]) in the audio file
def getAction():
    return sys.argv[2] if len(sys.argv) > 2 else None



# soju will look for this word in the audio file
def getTerm():
    return sys.argv[3] if len(sys.argv) > 3 else None














video_filename = getFile()
action = getAction()
term_to_find = getTerm()



list_of_words = []
if(video_filename is not None):
    audio_filename = "temp.wav"

    clip = VideoFileClip(video_filename, target_resolution=(1080, 1920))

    clipAudio = clip.audio
    clipAudio.write_audiofile(audio_filename, ffmpeg_params=["-ac", "1"])

    list_of_words = script.main(audio_filename, action, term_to_find)
    os.remove(audio_filename)



if((len(list_of_words) < 1)):
    print('no word was found or transcription completed')
else:
    image = ImageClip("{0}/image/vibecheckemoji.png".format(ASSETS_PATH), duration=.7)
    image = image.subclip(0, image.end).set_pos(("center","center")).resize((1920,1080)).crossfadeout(.5)

    goofyass_clip = clip
    for word in list_of_words:
        uppper_half = goofyass_clip.subclip(word.end, goofyass_clip.end)
        bottom_half = goofyass_clip.subclip(goofyass_clip.start, word.end)
        uppper_half = CompositeVideoClip([uppper_half, image])
        goofyass_clip = concatenate_videoclips([bottom_half, uppper_half])

    goofyass_clip.write_videofile(
        'output.mp4',
        fps=30,
        remove_temp=True,
        codec="libx264",
        audio_codec="aac",
        threads = 6,
    )
