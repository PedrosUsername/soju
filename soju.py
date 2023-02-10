import json
import sys

from utils import utils





# TODO - improve error messages
# TODO - add unit tests
# TODO - organize code and directories with formal design patterns
# TODO - add support for imgages with different sizes
# TODO - add support for image dramatic zoom in
# TODO - add video video composition
# TODO - organize ./settings/variables file by Vosk and moviePy (soju.json file generation / video edit configs)














def merge_audioarray_video(audioarray, video):
    for audio in audioarray:
        edit = utils.reach_goofy_audio(audio)

        video.audio = utils.merge_audio_video(
            video,
            edit
        )

    return video





def get_boomers():
    describe_json = []
    with open(utils.generate_soju_file_name(videofilepath), 'r') as f:
        describe_json = f.read()

    return json.loads(describe_json)["boomers"]





videofilepath = sys.argv[1] if len(sys.argv) > 1 else None
jsonfilepath = sys.argv[2] if len(sys.argv) > 2 else None





if(videofilepath is not None and jsonfilepath is None):
    clip = utils.get_and_prepare_clip_for_vosk_description(videofilepath)
    print("Soju - clip duration: {}".format(clip.duration))

    list_of_words = utils.voskDescribe()

    with open(utils.generate_soju_file_name(videofilepath), 'w') as f:
        f.writelines('{\n\t"data": [' + '\n')
        for i, word in enumerate(list_of_words):
            comma = ',' if i < (len(list_of_words) - 1) else ''
            f.writelines('\t\t{0}{1}\n'.format(word.to_string(), comma))
        f.writelines('\t],\n\n')
        f.writelines('\t"boomers": [\n\n\t]\n}')
    
    clip.close()





elif(videofilepath is not None and jsonfilepath is not None):
    boom_trigger = utils.get_boom_trigger()
    boomers = get_boomers()

    clip = utils.get_and_prepare_clip_for_moviepy_edition(videofilepath)

    for boomer in boomers:
        image = utils.reach_goofyahh_image(boomer)
        audioarray = boomer["audio"]["files"] if (boomer["audio"] is not None and boomer["audio"]["files"] is not None) else []

        if boomer["word"]["end"] > clip.start and boomer["word"]["start"] < clip.end:
            uppper_half = clip.subclip(boomer["word"][boom_trigger], clip.end)
            bottom_half = clip.subclip(clip.start, boomer["word"][boom_trigger])

            uppper_half = utils.merge_image_video(
                image,
                uppper_half,
                boomer,
                boomers
            )

            uppper_half = merge_audioarray_video(
                audioarray,
                uppper_half 
            )

            clip = utils.final_merge(bottom_half, uppper_half)
        elif boomer["word"]["end"] <= clip.start:
            uppper_half = clip.subclip(clip.start, clip.end)
            bottom_half = image
        elif boomer["word"]["start"] >= clip.end:
            uppper_half = image
            bottom_half = clip.subclip(clip.start, clip.end)        

    print("Soju - final clip duration: {0}".format(clip.duration))
    clip.write_videofile(
        utils.generate_output_file_name(videofilepath),
        fps=30
    )

    clip.close()
