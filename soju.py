import sys

from utils import vosk_utils, ffmpeg_utils





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
    vosk_utils.soju(videofilepath)

elif(videofilepath is not None and jsonfilepath is not None):
    ffmpeg_utils.soju(videofilepath, jsonfilepath)
    result = vosk_utils.soju2(videofilepath, jsonfilepath)

    print("\nSoju - final clip duration in seconds: {:.2f}\n".format(result.duration))
    result.write_videofile(
        vosk_utils.generate_output_file_name(videofilepath),
        fps= 30
    )
