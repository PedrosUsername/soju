import sys

from utils import utils





# TODO - improve error messages
# TODO - add unit tests
# TODO - organize code and directories with formal design patterns and classes

# TODO - wrong variables.DEFAULT_IMAGE_PATH name returns loop
# TODO - implement deep folder file search
# TODO - organize ./settings/variables file by Vosk and moviePy (soju.json file generation / video edit configs)
# TODO - add support for image dramatic zoom in






















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
    boomers = utils.get_boomers(videofilepath, jsonfilepath)

    clip = utils.get_and_prepare_clip_for_moviepy_edition(videofilepath)

    for boomer in boomers:
        boom_trigger = utils.get_boom_trigger(boomer)
        image = utils.reach_goofyahh_image(boomer)
        audioarray = boomer["audio"]["files"] if (boomer["audio"] is not None and boomer["audio"]["files"] is not None) else []

        print("\n")
        print('Soju - Working on boomer [ "{}" ]'.format(boomer["word"]["content"]))
        print("""soju - Boomin' at second [ {:.2f} ]""".format(boomer["word"][boom_trigger]))
        print("""soju - visual media [ {} ]""".format(boomer["image"]["file"]))
        print("""soju - audio media [ {} ]""".format(str(audioarray)))
        print("\n")

        if boomer["word"]["end"] > clip.start and boomer["word"]["start"] < clip.end:
            uppper_half = clip.subclip(boomer["word"][boom_trigger], clip.end)
            bottom_half = clip.subclip(clip.start, boomer["word"][boom_trigger])

            uppper_half = utils.merge_image_video(
                image,
                uppper_half,
                boomer,
                boomers
            )

            uppper_half = utils.merge_audioarray_video(
                audioarray,
                uppper_half,
                boomer
            )
            clip = utils.final_merge(bottom_half, uppper_half)
            
        elif boomer["word"]["end"] <= clip.start:
            uppper_half = clip.subclip(clip.start, clip.end)
            bottom_half = image

            bottom_half = utils.merge_audioarray_video(
                audioarray,
                bottom_half,
                boomer
            )

            utils.clip_extend(boomers, boomer["image"]["conf"]["max_duration"])

            clip = utils.final_merge(bottom_half, uppper_half)

        elif boomer["word"]["start"] >= clip.end:
            uppper_half = image
            bottom_half = clip.subclip(clip.start, clip.end)

            boomer["image"]["conf"]["imageconcatstrategy"] = utils.ImageMergeStrategy.CONCAT_ENUM

            uppper_half = utils.merge_audioarray_video(
                audioarray,
                uppper_half,
                boomer
            )

            clip = utils.final_merge(bottom_half, uppper_half)

    print("\nSoju - final clip duration in seconds: {:.2f}\n".format(clip.duration))
    clip.write_videofile(
        utils.generate_output_file_name(videofilepath),
        fps= 30,
        threads= 4
    )

    clip.close()
