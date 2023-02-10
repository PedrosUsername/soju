import json
import sys

from utils import utils





# TODO - organize code and directories with some design pattern
# TODO - add video video composition
# TODO - audio volume controls















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
        f.writelines('\t"goofywords": [\n\n\t]\n}')
    
    clip.close()





elif(videofilepath is not None and jsonfilepath is not None):
    goofy_trigger = utils.get_trigger_settings()

    describe_json = []
    with open(utils.generate_soju_file_name(videofilepath), 'r') as f:
        describe_json = f.read()

    describe_goofywords = json.loads(describe_json)["goofywords"]

    clip = utils.get_and_prepare_clip_for_moviepy_edition(videofilepath)

    for word in describe_goofywords:
        image = utils.get_goofy_image(word)

        uppper_half = clip.subclip(word[goofy_trigger], clip.end)
        bottom_half = clip.subclip(clip.start, word[goofy_trigger])

        uppper_half = utils.merge_visuals(
            uppper_half,
            image,
            word,
            describe_goofywords
        )
        
        goofy_audios = word["audio"] if word["audio"] is not None else []
        for goofy_audio in goofy_audios:
            audio = utils.get_goofy_audio(goofy_audio)

            uppper_half.audio = utils.merge_sounds(
                uppper_half,
                audio,
            )
        
        clip = utils.final_merge(bottom_half, uppper_half)

    print("Soju - final clip duration: {0}".format(clip.duration))
    clip.write_videofile(
        utils.generate_output_file_name(videofilepath),
        fps=30
    )

    clip.close()
