# goofy confs
BOOM_AT_WORD_END = False
ALLOW_IMAGE_REPETITION_WHEN_RANDOM = False

# image confs
DEFAULT_IMAGE_PATH = "./assets/image/pettan/"
DEFAULT_IMAGE_FILE = "vibecheckemojialt.png"
DEFAULT_NULL_IMAGE_FILE = "./assets/image/null.png"
CHOOSE_IMAGE_AT_RANDOM = 1                     # 0     -> use image DEFAULT_IMAGE_FILE for every word
                                               # n > 0 -> use Random images for every word
MAX_IMAGE_DURATION = .9

IGNORE_IMAGE_FILE_LIST = [
    DEFAULT_NULL_IMAGE_FILE
]


# audio confs
DEFAULT_AUDIO_PATH = "./assets/audio/"
DEFAULT_AUDIO_FILE = ["vineboom.mp3"]
DEFAULT_NULL_AUDIO_FILE = "./assets/audio/null.mp3"
CHOOSE_AUDIO_AT_RANDOM = 0                     # 0     -> add only DEFAULT_AUDIO_FILE sounds
                                               # n > 0 -> add DEFAULT_AUDIO_FILE + n random sounds
MAX_AUDIO_DURATION = 1.36

IGNORE_AUDIO_FILE_LIST = [
    DEFAULT_NULL_AUDIO_FILE
]


# general confs
PATH_MODEL = "./models/en-model"

DEFAULT_OUTPUT_PATH = "./"

PATH_DEFAULT_JSON_FILE = "./assets/json/"

PATH_TMP_AUDIO = "./utils/settings/tmp_audio_file.wav"
