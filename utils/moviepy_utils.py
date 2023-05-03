import time
import ntpath
import filetype
import tempfile

from moviepy.editor import *

from .settings import variables
from . import ffmpeg_utils, vosk_utils, boomer_utils as bu















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
















def makeItGoofyForDiscord(moviepycopy="moviepy_friendly_copy.mp4", main_input_url="", sojufile= None, tmp_dir= "./") :

    boomers = bu.get_boomers_from_dict(sojufile)

    if len(boomers) < 1 :
        raise Exception("boomers list is empty")

    og_clip = getClipWithMoviePy(moviepycopy)
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

















def buildSojuFileForDiscord(videofilepath= None, sojufile= None, random_media= ([], [], []), tmp_dir= "./") :
    if(videofilepath is not None):
        tmp_audio_path = tmp_dir + variables.TMP_AUDIO_FILE_NAME
        ffmpeg_utils.get_only_audio(videofilepath, tmp_audio_path)

        if AudioFileClip(tmp_audio_path).duration > 59.90 :
            raise Exception("media duration exceeds the current limit")


        list_of_words = vosk_utils.voskDescribe(
            audio_file_path= tmp_audio_path,
            generator= bu.get_boomer_generator_from_dict(sojufile)
        )

        filename = generate_soju_file_name(videofilepath, tmp_dir)

        with open(filename, 'w') as f :
            f.writelines(
f"""
{{
 	"soju": {{
     
        "boomers": [

        ],

		"generated": [
"""
            )
            
            for i, word in enumerate(list_of_words):
                comma = ',' if i < (len(list_of_words) - 1) else ''
                f.writelines('\t\t\t{0}{1}\n'.format(word.to_string(), comma))

            f.writelines(
"""
        ]

    }
}            
"""         )

        
        return filename






























































