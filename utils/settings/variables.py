# image confs
DEFAULT_IMAGE_PATH = "./assets/image/"
DEFAULT_IMAGE_FILE = "vibecheckemojialt.png"
DEFAULT_NULL_IMAGE_FILE = "null.png"
CHOOSE_IMAGE_AT_RANDOM = 1                     # 0     -> use image DEFAULT_IMAGE_FILE for every word
                                               # n > 0 -> use Random images for every word
MAX_IMAGE_DURATION = 1.1

IGNORE_IMAGE_FILE_LIST = [
    DEFAULT_NULL_IMAGE_FILE
]


# audio confs
DEFAULT_AUDIO_PATH = "./assets/audio/"
DEFAULT_AUDIO_FILE = ["vineboom.mp3"]
DEFAULT_NULL_AUDIO_FILE = "null.mp3"
CHOOSE_AUDIO_AT_RANDOM = 2                     # 0     -> add only DEFAULT_AUDIO_FILE sounds
                                               # n > 0 -> add DEFAULT_AUDIO_FILE + n random sounds
MAX_AUDIO_DURATION = 2.45

IGNORE_AUDIO_FILE_LIST = [
    DEFAULT_NULL_AUDIO_FILE
]


# general confs
PATH_MODEL = "./models/en-model"

PATH_DEFAULT_OUTPUT = "output.mp4"

PATH_DEFAULT_JSON_FILE = "edit.soju.json"

PATH_TMP_AUDIO = "./utils/settings/tmp_audio_file.wav"
