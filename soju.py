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





utils.soju(videofilepath, jsonfilepath)