import os
import json

from utils import utils
from utils.settings import variables
from moviepy.editor import *





# TODO - organizar codigo de acordo com algum design pattern





videofile = sys.argv[1] if len(sys.argv) > 1 else None
jsonfile = sys.argv[2] if len(sys.argv) > 2 else None



if(videofile is not None and jsonfile is None):
    clip = VideoFileClip(videofile, target_resolution=(1080, 1920))
    clip.audio.write_audiofile(variables.PATH_TMP_AUDIO, ffmpeg_params=["-ac", "1"])

    list_of_words = utils.voskDescribe(variables.PATH_TMP_AUDIO, variables.PATH_MODEL)
    os.remove(variables.PATH_TMP_AUDIO)

    with open(variables.PATH_DEFAULT_JSON_FILE, 'w') as f:
        f.writelines('{\n\t"data": [' + '\n')
        for i, word in enumerate(list_of_words):
            comma = ',' if i < (len(list_of_words) - 1) else ''
            f.writelines('\t\t{0}{1}\n'.format(word.to_string(), comma))
        f.writelines('\t],\n\n')
        f.writelines('\t"goofywords": []\n}')
    
    clip.close()

elif(videofile is not None and jsonfile is not None):    
    describe_json = []
    with open(variables.PATH_DEFAULT_JSON_FILE, 'r') as f:
        describe_json = f.read()

    describe_data = json.loads(describe_json)["data"]
    describe_goofywords = json.loads(describe_json)["goofywords"]
    describe_data_filtered = [e for e in describe_data if e["word"] in describe_goofywords]

    clip = VideoFileClip(videofile, target_resolution=(1080, 1920))

    for word in describe_data_filtered:
        goofy_image = '{0}{1}'.format(variables.PATH_DEFAULT_IMAGE, word["image"]) if word["image"] is not None else variables.PATH_NULL_IMAGE
        goofy_audios = word["audio"] if word["audio"] is not None else []

        image = ImageClip(goofy_image, duration=.7)
        image = image.subclip(0, image.end).set_pos(("center","center")).resize((1920, 1080)).crossfadeout(.5)
        
        uppper_half = clip.subclip(word["end"], clip.end)
        uppper_half = CompositeVideoClip([uppper_half, image])
        
        for goofy_audio in goofy_audios:
            goofy_audio = '{0}{1}'.format(variables.PATH_DEFAULT_AUDIO, goofy_audio) if goofy_audio is not None else variables.PATH_NULL_AUDIO
            audio = AudioFileClip(goofy_audio)
            audio = audio.subclip(0, variables.DEFAULT_MAX_IMG_DURATION) if audio.duration > variables.DEFAULT_MAX_IMG_DURATION else audio.subclip(0, audio.end)
            uppper_half.audio = CompositeAudioClip([uppper_half.audio, audio])
        
        bottom_half = clip.subclip(clip.start, word["end"])
        clip = concatenate_videoclips([bottom_half, uppper_half])

    clip.write_videofile(
        variables.PATH_DEFAULT_OUTPUT,
        fps=30
    )

    clip.close()
