# start   -> boom will be inserted at ["boomers"]["word"]["start"] seconds
# end     -> boom will be inserted at ["boomers"]["word"]["end"] seconds
DEFAULT_BOOM_TRIGGER = "START"
DEFAULT_BOOMIN_TIME = 0









# ########################################## soju.json IMAGE CONF.

DEFAULT_IMAGE_MERGE_STRATEGY = "COMPOSE"          # COMPOSE | CONCAT

DEFAULT_IMAGE_FOLDER = "./assets/image/default/"
ALLOW_IMAGE_REPETITION = True
IGNORE_IMAGE_FILE_LIST = []
DEFAULT_IMAGE_DIR = "DEFAULT"

DEFAULT_IMAGE_FILE = None

DEFAULT_IMAGE_DURATION = 0.8
DEFAULT_IMAGE_TRIGGER_DELAY = 0

DEFAULT_IMAGE_RESOLUTION_HEIGHT = 1080               # 1080 px | 0 | -n
DEFAULT_IMAGE_RESOLUTION_WIDTH = None                # http://trac.ffmpeg.org/wiki/Scaling
DEFAULT_IMAGE_POSITION_X = "CENTER"                       # float relative to screen size
DEFAULT_IMAGE_POSITION_Y = "CENTER"                       # https://zulko.github.io/moviepy/getting_started/compositing.html?highlight=position#positioning-clips

# ################################################################










# ########################################## soju.json AUDIO CONF.

DEFAULT_AUDIO_FOLDER = "./assets/audio/default/"
ALLOW_AUDIO_REPETITION = True
IGNORE_AUDIO_FILE_LIST = []
DEFAULT_AUDIO_DIR = "DEFAULT"

DEFAULT_AUDIO_FILE = None

DEFAULT_AUDIO_DURATION = 0.8
DEFAULT_AUDIO_TRIGGER_DELAY = 0
DEFAULT_AUDIO_VOLUME = 1

DEFAULT_NULL_AUDIO_FILE = "./assets/audio/null.mp3"

# ################################################################
















# ########################################## soju.json VIDEO CONF.

DEFAULT_VIDEO_MERGE_STRATEGY = "CONCAT"          # COMPOSE | CONCAT

DEFAULT_VIDEO_FOLDER = "./assets/video/default/"
ALLOW_VIDEO_REPETITION = True
IGNORE_VIDEO_FILE_LIST = []
DEFAULT_VIDEO_DIR = "DEFAULT"

DEFAULT_VIDEO_FILE = None

DEFAULT_VIDEO_DURATION = 0.8
DEFAULT_VIDEO_TRIGGER_DELAY = 0
DEFAULT_VIDEO_VOLUME = 0

DEFAULT_VIDEO_RESOLUTION_HEIGHT = 1080               # 1080 px | 0 | -n
DEFAULT_VIDEO_RESOLUTION_WIDTH = None                # http://trac.ffmpeg.org/wiki/Scaling
DEFAULT_VIDEO_POSITION_X = "CENTER"                         # float relative to screen size
DEFAULT_VIDEO_POSITION_Y = "CENTER"                         # https://zulko.github.io/moviepy/getting_started/compositing.html?highlight=position#positioning-clips

# ################################################################









# general confs
INTERVAL_DIFF_NOVOSK_DESCRIBE = 7
OVERLAY_SIZE_TOLERANCE = 69
MAX_MEDIA_INSERT_DURATION = 8
MAX_MEDIA_DELAY = 8
MAX_MEDIA_VOLUME = 1

DEFAULT_API_NAME = "VOSK"
DEFAULT_API_MODEL = "en-128"
OUTPUT_RESOLUTION_HEIGHT = 0               # http://trac.ffmpeg.org/wiki/Scaling
OUTPUT_RESOLUTION_WIDTH = 0                # 1920 px | -n | 0

PATH_MODEL = "/home/pedro/Downloads/sojubot/models/en/lightweight"   
DEFAULT_OUTPUT_PATH = ""
PATH_DEFAULT_JSON_FILE = "./assets/json/"







# ffmpeg confs
FFMPEG_PATH = "/snap/bin/ffmpeg" # whereis ffmpeg
FFMPEG_FPS = "30"
FFMPEG_VIDEO_CODEC = "h264"
FFMPEG_AUDIO_CODEC = "aac"
FFMPEG_VIDEO_BITRATE = "64k"
FFMPEG_AUDIO_BITRATE = "196k"
FFMPEG_SAMPLE_RATE = "44100"
FFMPEG_ENCODING_SPEED = "fast"
FFMPEG_CRF = "22"
FFMPEG_FRAME_SIZE = "1280x720"
FFMPEG_PIX_FMT = "yuv420p"
FFMPEG_VTTS = "90000"

FFMPEG_OUTPUT_SPECS=  [
    "-c:v",
    FFMPEG_VIDEO_CODEC,
    "-c:a",
    FFMPEG_AUDIO_CODEC,
    "-b:v",
    FFMPEG_VIDEO_BITRATE,
    "-b:a",
    FFMPEG_AUDIO_BITRATE,
    "-preset",
    FFMPEG_ENCODING_SPEED,
    "-crf",
    FFMPEG_CRF,
#    "-s",
#    FFMPEG_FRAME_SIZE,
    "-ar",
    FFMPEG_SAMPLE_RATE,
    "-pix_fmt",
    FFMPEG_PIX_FMT,
    "-video_track_timescale",
    FFMPEG_VTTS,
    "-r",
    FFMPEG_FPS
]







# program variables
TMP_AUDIO_FILE_NAME = "tmp_audio.wav"
DEFAULT_TMP_FILE_PATH = "./utils/settings/tmp/"
MIN_MEDIA_VOLUME = 0
MIN_MEDIA_INSERT_DURATION = 0
MIN_MEDIA_DELAY = 0
MIN_RESOLUTION_SIZE = 0