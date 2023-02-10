import json
import sys

from utils import utils





# TODO - improve error messages
# TODO - add unit tests
# TODO - organize code and directories with formal design patterns
# TODO - add video video composition
# TODO - organize ./settings/variables file by Vosk and moviePy (soju.json file generation / video edit configs)
# TODO - dict / json words should support the attr "image" : { "file": null, "confs": { "duration": null, "imageconcatstrategy": null } }
# TODO - dict / json words should support the attr "audio" : { "file": null, "confs": { "duration": null, "volume": null } }














def merge_audioarray_video(audioarray, video, word):
    for audio in audioarray:
        edit = utils.reach_goofy_audio(audio)

        video.audio = utils.merge_audio_video(
            video,
            edit
        )

    return video





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
    goofy_trigger = utils.get_trigger_settings()

    describe_json = []
    with open(utils.generate_soju_file_name(videofilepath), 'r') as f:
        describe_json = f.read()

    describe_goofywords = json.loads(describe_json)["boomers"]

    clip = utils.get_and_prepare_clip_for_moviepy_edition(videofilepath)

    for word in describe_goofywords:
        image = utils.get_goofy_image(word)
        audioarray = word["audio"] if word["audio"] is not None else []


        if word["end"] > clip.start and word["start"] < clip.end:
            uppper_half = clip.subclip(word[goofy_trigger], clip.end)
            bottom_half = clip.subclip(clip.start, word[goofy_trigger])


            uppper_half = utils.merge_image_video(
                image,
                uppper_half,
                word,
                describe_goofywords
            )

            uppper_half = merge_audioarray_video(
                audioarray,
                uppper_half,
                word                
            )

            clip = utils.final_merge(bottom_half, uppper_half)
        elif word["end"] <= clip.start:
            uppper_half = clip.subclip(clip.start, clip.end)
            bottom_half = image
        elif word["start"] >= clip.end:
            uppper_half = image
            bottom_half = clip.subclip(clip.start, clip.end)        

    print("Soju - final clip duration: {0}".format(clip.duration))
    clip.write_videofile(
        utils.generate_output_file_name(videofilepath),
        fps=30
    )

    clip.close()
