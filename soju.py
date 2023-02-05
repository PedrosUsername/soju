import os
import json
import utils

from moviepy.editor import *



MODEL_PATH = "./models/en-model"
TMP_AUDIO = "tmp_audio_file.wav"
DESCRIBE_JSON_FILE_NAME = "./settings/goofywords.json"









videofile = sys.argv[1] if len(sys.argv) > 1 else None
wordlistfile = sys.argv[2] if len(sys.argv) > 2 else None



if(videofile is not None and wordlistfile is None):
    clip = VideoFileClip(videofile, target_resolution=(1080, 1920))
    clip.audio.write_audiofile(TMP_AUDIO, ffmpeg_params=["-ac", "1"])

    list_of_words = utils.voskDescribe(TMP_AUDIO, MODEL_PATH)
    os.remove(TMP_AUDIO)

    with open(DESCRIBE_JSON_FILE_NAME, 'w') as f:
        f.writelines('{\n\t"data": [' + '\n')
        for i, word in enumerate(list_of_words):
            comma = ',' if i < (len(list_of_words) - 1) else ''
            f.writelines('\t\t{0}{1}\n'.format(word.to_string(), comma))
        f.writelines('\t],\n\n')
        f.writelines('\t"goofywords": []\n}')

elif(videofile is not None and wordlistfile is not None):    
    describe_json = []
    with open(DESCRIBE_JSON_FILE_NAME, 'r') as f:
        describe_json = f.read()

    describe_data = json.loads(describe_json)["data"]
    describe_goofywords = json.loads(describe_json)["goofywords"]
    describe_data_filtered = [e for e in describe_data if e["word"] in describe_goofywords]

    clip = VideoFileClip(videofile, target_resolution=(1080, 1920))

    goofyahh_clip = clip
    for word in describe_data_filtered:
        image = ImageClip("./assets/image/vibecheckemoji.png", duration=.7)
        image = image.subclip(0, image.end).set_pos(("center","center")).resize((1920, 1080)).crossfadeout(.5)

        uppper_half = goofyahh_clip.subclip(word["end"], goofyahh_clip.end)
        bottom_half = goofyahh_clip.subclip(goofyahh_clip.start, word["end"])
        uppper_half = CompositeVideoClip([uppper_half, image])
        goofyahh_clip = concatenate_videoclips([bottom_half, uppper_half])

    goofyahh_clip.write_videofile(
        'output.mp4',
        fps=30,
        remove_temp=True,
        codec="libx264",
        audio_codec="aac",
        threads = 6,
    )
