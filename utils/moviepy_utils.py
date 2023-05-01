import time
import ntpath
import filetype
import tempfile

from moviepy.editor import *

from .settings import variables
from . import ImageMergeStrategy, ffmpeg_utils, vosk_utils, boomer_utils as bu















def get_base_file_name_from(videofilepath):
    filename = ntpath.basename(videofilepath)
    head, tail = filename[::-1].split(".", 1)
    return tail[::-1]





def generate_soju_file_name(videofilepath, path= None):
    videofilename = get_base_file_name_from(videofilepath)

    pathtofile = path if path else variables.PATH_DEFAULT_JSON_FILE
    return "{}{}.soju.json".format(pathtofile, videofilename)






def generate_output_file_name(videofilepath, path= None):
    videofilename = get_base_file_name_from(videofilepath)

    pathtofile = path if path else variables.DEFAULT_OUTPUT_PATH
    return "{}{}.mp4".format(pathtofile, videofilename)








def isVideo(our_file):
    kind = filetype.guess(our_file)
    if kind is None:
        print('Cannot guess file type!')
        return False
    
    if kind.extension != "ogv" and kind.extension != "mp4" and kind.extension != "mpeg" and kind.extension != "avi" and kind.extension != "mov":
        return False
    else:
        return True









def getClipWithMoviePy(videofilepath, audio= True):
    return VideoFileClip(
        videofilepath,
        audio= audio
    )












def makeItGoofy(videofilepath="", jsonfilepath= None):
    time_start = time.time()

    og_clip = getClipWithMoviePy(videofilepath)
    boomers = bu.get_boomers(jsonfilepath)

    boomers_top, boomers_mid, boomers_bot = bu.filterBoomers(og_clip.duration, boomers)

    if len(boomers_mid) > 0:
        outputfilename = generate_output_file_name(videofilepath)

        og_clip_params = {
            "file": videofilepath,
            "duration": og_clip.duration,
            "width": og_clip.size[0],
            "height": og_clip.size[1]
        }
        
        call_params = ffmpeg_utils.buildCall(og_clip_params, outputfilename, boomers_mid)
        
        for p in call_params:
            print(str(p), end= "\n\n\n")

        ffmpeg_utils.executeFfmpegCall(
            params= call_params
        )

    time_end = time.time() - time_start
    print("\nclip is ready! it took {:.2f} seconds to make it goofy".format(time_end))
















def makeItGoofyForDiscord(moviepycopy="moviepy_friendly_copy.mp4", main_input_url="",jsonfilepath= None, tmp_dir= "./") :

    og_clip = getClipWithMoviePy(moviepycopy)
    boomers = bu.get_boomers_from_url(jsonfilepath)

    boomers_top, boomers_mid, boomers_bot = bu.filterBoomers(og_clip.duration, boomers)
    outputfilename = generate_output_file_name(main_input_url, tmp_dir)

    og_clip_params = {
        "file": main_input_url,
        "duration": og_clip.duration,
        "width": og_clip.size[0],
        "height": og_clip.size[1]
    }
    
    call_params = ffmpeg_utils.buildCall(og_clip_params, outputfilename, boomers_mid)
    
    for p in call_params :
        print(str(p), end= "\n\n\n")

    ffmpeg_utils.executeFfmpegCall(params= call_params)

    return outputfilename












def buildSojuFile(videofilepath= None, jsonfilepath= None, outputfile= None):
    if(videofilepath is not None and jsonfilepath is None):
        with tempfile.TemporaryDirectory(dir="./") as tmp_dir:
            ffmpeg_utils.get_only_audio(videofilepath, tmp_dir + "/" + variables.TMP_AUDIO_FILE_NAME)

            list_of_words = vosk_utils.voskDescribe(tmp_dir + "/" + variables.TMP_AUDIO_FILE_NAME)

        filename = generate_soju_file_name(videofilepath) if outputfile is None else outputfile

        with open(filename, 'w') as f:
            f.writelines('{\n\t"description": [' + '\n')
            for i, word in enumerate(list_of_words):
                comma = ',' if i < (len(list_of_words) - 1) else ''
                f.writelines('\t\t{0}{1}\n'.format(word.to_string(), comma))
            f.writelines('\t],\n\n')
            f.writelines('\t"boomers": [\n\n\t]\n}')
        
        return None

















async def buildSojuFileForDiscord(videofilepath= None, jsonfilepath= None, random_media= ([], [], []), tmp_dir= "./"):
    if(videofilepath is not None and jsonfilepath is None):
        ffmpeg_utils.get_only_audio(videofilepath, tmp_dir + variables.TMP_AUDIO_FILE_NAME)
        list_of_words = vosk_utils.voskDescribe(tmp_dir + variables.TMP_AUDIO_FILE_NAME)

        filename = generate_soju_file_name(videofilepath, tmp_dir)

        with open(filename, 'w') as f:
            f.writelines("""
{
 	"soju": {

		"generator": {
			"defaults": {
				"word": {
					"trigger": "start"
				},

				"image": {
					"FILE": "RANDOM",
					"MERGESTRATEGY": "COMPOSE",
					"DURATION": 0.3,
					"HEIGHT": 440,
					"WIDTH": null,               
					"POSX": "RANDOM",
					"POSY": "RANDOM",
					"triggerdelay": 0
				},
		
				"video": {
					"FILE": "RANDOM",
					"MERGESTRATEGY": "COMPOSE",
					"DURATION": 0.3,
					"HEIGHT": 440,
					"WIDTH": null,               
					"POSX": "RANDOM",
					"POSY": "RANDOM",
					"triggerdelay": 0.1,
					"VOLUME": 0
				},
		
				"audio": {
					"FILE": "RANDOM",
					"DURATION": 0.3,
					"triggerdelay": 0,
					"VOLUME": 0
				},
		
				"general": {
					"RESOTOLERANCE": 69,

					"API": {
						"name": "VOSK",
						"model": "en-model-128"
					}		
				}
			}
		},

		"generated": [
""")
            for i, word in enumerate(list_of_words):
                comma = ',' if i < (len(list_of_words) - 1) else ''
                f.writelines('\t\t\t{0}{1}\n'.format(word.to_string(), comma))

            f.writelines("""
        ],

        "boomers": [

        ]
    }
}            
            """)

        
        return filename






























































