import os
import json

from utils import utils
from moviepy.editor import *



DEFAULT_IMAGE = "./assets/image/vibecheckemojialt.png"
DEFAULT_AUDIO = "./assets/audio/vineboom.mp3"
DEFAULT_MAX_IMAGE_DURATION = 1.38
DEFAULT_OUTPUT_PATH = 'output.mp4'
DEFAULT_JSON_FILE_NAME = "soju.edit.json"

MODEL_PATH = "./models/en-model"
TMP_AUDIO = "tmp_audio_file.wav"









videofile = sys.argv[1] if len(sys.argv) > 1 else None
jsonfile = sys.argv[2] if len(sys.argv) > 2 else None



if(videofile is not None and jsonfile is None):
    clip = VideoFileClip(videofile, target_resolution=(1080, 1920))
    clip.audio.write_audiofile(TMP_AUDIO, ffmpeg_params=["-ac", "1"])

    list_of_words = utils.voskDescribe(TMP_AUDIO, MODEL_PATH)
    os.remove(TMP_AUDIO)

    with open(DEFAULT_JSON_FILE_NAME, 'w') as f:
        f.writelines('{\n\t"data": [' + '\n')
        for i, word in enumerate(list_of_words):
            comma = ',' if i < (len(list_of_words) - 1) else ''
            f.writelines('\t\t{0}{1}\n'.format(word.to_string(), comma))
        f.writelines('\t],\n\n')
        f.writelines('\t"goofywords": []\n}')
    
    clip.close()

elif(videofile is not None and jsonfile is not None):    
    describe_json = []
    with open(DEFAULT_JSON_FILE_NAME, 'r') as f:
        describe_json = f.read()

    describe_data = json.loads(describe_json)["data"]
    describe_goofywords = json.loads(describe_json)["goofywords"]
    describe_data_filtered = [e for e in describe_data if e["word"] in describe_goofywords]

    clip = VideoFileClip(videofile, target_resolution=(1080, 1920))

    for word in describe_data_filtered:
        goofy_image = word["image"] if word["image"] is not None else DEFAULT_IMAGE
        goofy_audio = word["audio"] if word["audio"] is not None else DEFAULT_AUDIO

        image = ImageClip(goofy_image, duration=.7)
        image = image.subclip(0, image.end).set_pos(("center","center")).resize((1920, 1080)).crossfadeout(.5)

        audio = AudioFileClip(goofy_audio)
        audio = audio.subclip(0, DEFAULT_MAX_IMAGE_DURATION) if audio.duration > DEFAULT_MAX_IMAGE_DURATION else audio.subclip(0, audio.end)

        uppper_half = clip.subclip(word["end"], clip.end)

        uppper_half = CompositeVideoClip([uppper_half, image])
        uppper_half.audio = CompositeAudioClip([uppper_half.audio, audio])
        
        bottom_half = clip.subclip(clip.start, word["end"])
        clip = concatenate_videoclips([bottom_half, uppper_half])

    clip.write_videofile(
        DEFAULT_OUTPUT_PATH,
        fps=30
    )

    clip.close()
