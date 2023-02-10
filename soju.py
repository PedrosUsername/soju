import os
import json

from utils import utils, ImageMergeStrategy
from utils.settings import variables
from moviepy.editor import *





# TODO - organize code and directories with some fancy design pattern
# TODO - add video video composition
# TODO - audio volume controls




videofilepath = sys.argv[1] if len(sys.argv) > 1 else None
jsonfilepath = sys.argv[2] if len(sys.argv) > 2 else None



if(videofilepath is not None and jsonfilepath is None):
    clip = VideoFileClip(videofilepath, target_resolution=(1080, 1920))
    print("Soju - clip duration: {}".format(clip.duration))
    clip.audio.write_audiofile(variables.PATH_TMP_AUDIO, ffmpeg_params=["-ac", "1"])

    list_of_words = utils.voskDescribe(variables.PATH_TMP_AUDIO, variables.PATH_MODEL)
    os.remove(variables.PATH_TMP_AUDIO)

    with open(utils.generate_soju_file_name(videofilepath), 'w') as f:
        f.writelines('{\n\t"data": [' + '\n')
        for i, word in enumerate(list_of_words):
            comma = ',' if i < (len(list_of_words) - 1) else ''
            f.writelines('\t\t{0}{1}\n'.format(word.to_string(), comma))
        f.writelines('\t],\n\n')
        f.writelines('\t"goofywords": [\n\n\t]\n}')
    
    clip.close()

elif(videofilepath is not None and jsonfilepath is not None):
    goofy_trigger = "end" if variables.BOOM_AT_WORD_END else "start"

    describe_json = []
    with open(utils.generate_soju_file_name(videofilepath), 'r') as f:
        describe_json = f.read()

    describe_goofywords = json.loads(describe_json)["goofywords"]

    clip = VideoFileClip(videofilepath, target_resolution=(1080, 1920))

    for word in describe_goofywords:
        goofy_image = '{0}{1}'.format(variables.DEFAULT_IMAGE_PATH, word["image"]) if word["image"] is not None else variables.DEFAULT_NULL_IMAGE_FILE
        goofy_audios = word["audio"] if word["audio"] is not None else []

        image = ImageClip(goofy_image, duration= variables.MAX_IMAGE_DURATION)
        image = image.subclip(0, image.end).set_pos(("center","center")).resize((1920, 1080)).crossfadeout(.5)
        
        uppper_half = clip.subclip(word[goofy_trigger], clip.end)
        bottom_half = clip.subclip(clip.start, word[goofy_trigger])

        if word["imageconcatstrategy"] == ImageMergeStrategy.CONCAT_ENUM:
            uppper_half = concatenate_videoclips([image, uppper_half])
            for word_again in describe_goofywords:
                word_again["start"] = word_again["start"] + variables.MAX_IMAGE_DURATION
                word_again["end"] = word_again["end"] + variables.MAX_IMAGE_DURATION

        else:
            uppper_half = CompositeVideoClip([uppper_half, image])
        
        for goofy_audio in goofy_audios:
            goofy_audio = '{0}{1}'.format(variables.DEFAULT_AUDIO_PATH, goofy_audio) if goofy_audio is not None else variables.DEFAULT_NULL_AUDIO_FILE
            audio = AudioFileClip(goofy_audio)
            audio = audio.subclip(0, variables.MAX_AUDIO_DURATION) if audio.duration > variables.MAX_AUDIO_DURATION else audio.subclip(0, audio.end)
            audio = audio.fx(afx.audio_fadeout, audio.duration * (2/3))

            uppper_half.audio = CompositeAudioClip([uppper_half.audio, audio])
        
        clip = concatenate_videoclips([bottom_half, uppper_half])

    print("Soju - final clip duration: {0}".format(clip.duration))
    clip.write_videofile(
        utils.generate_output_file_name(videofilepath),
        fps=30
    )

    clip.close()
