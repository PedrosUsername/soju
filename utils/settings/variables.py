# goofy confs
BOOM_AT_WORD_END = False
DEFAULT_IMAGE_CONCAT_STRATEGY = "COMPOSE"      # COMPOSE -> image will play with video (overlaped)
                                               # CONCAT  -> image will interrupt video to show up

# image confs
DEFAULT_IMAGE_PATH = "./assets/image/mommy/"
DEFAULT_IMAGE_FILE = "mio.png"
DEFAULT_NULL_IMAGE_FILE = "./assets/image/null.png"
ALLOW_IMAGE_REPETITION = True                  # ignored when not CHOOSE_IMAGE_AT_RANDOM 
CHOOSE_IMAGE_AT_RANDOM = 0                     # 0     -> use image DEFAULT_IMAGE_FILE for every word
                                               # n > 0 -> use Random images for every word
MAX_IMAGE_DURATION = .9
DEFAULT_IMAGE_RESOLUTION_HEIGHT = 1080               # 1080 px
DEFAULT_IMAGE_RESOLUTION_WIDTH = 1920                # 1920 px

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
DEFAULT_VOLUME = 1

IGNORE_AUDIO_FILE_LIST = [
    DEFAULT_NULL_AUDIO_FILE
]


# general confs
OUTPUT_RESOLUTION_HEIGHT = 1080
OUTPUT_RESOLUTION_WIDTH = 1920

PATH_MODEL = "./models/en-model"

DEFAULT_OUTPUT_PATH = "./"

PATH_DEFAULT_JSON_FILE = "./assets/json/"

PATH_TMP_AUDIO = "./utils/settings/tmp_audio_file.wav"
