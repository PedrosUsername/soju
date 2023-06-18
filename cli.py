import tempfile
import asyncio
import sys

from utils import moviepy_utils, ffmpeg_utils, file_utils, vosk_utils, boomer_utils as bu



























    





async def audio_descriptor(videofilepath, sojufile) :
    if videofilepath is None :
        raise Exception("clip not found")

    with tempfile.TemporaryDirectory(dir="./") as tmp_dir :
        ephemeral = tmp_dir + "/"

        main_clip_name = file_utils.get_base_file_name_from(videofilepath)
        full_main_clip_file_path = videofilepath

        moviepy_utils.init_og_clip_params(full_main_clip_file_path)




        full_aux_audio_file_path = ephemeral + main_clip_name + ".wav"
        full_new_soju_file_path = "./" + main_clip_name + ".soju.json"

        ffmpeg_utils.get_only_audio(full_main_clip_file_path, full_aux_audio_file_path)


        boomers = await vosk_utils.describe(
            audio_file_path= full_aux_audio_file_path,
            generator= bu.get_boomer_generator_from_dict(sojufile)
        )

        bu.build_sojufile_for_discord(full_new_soju_file_path, boomers)    



def video_editor(videofilepath= None, boomers= []) :
    if videofilepath is None :
        raise Exception("clip not found")

    with tempfile.TemporaryDirectory(dir="./") as tmp_dir :
        ephemeral = tmp_dir + "/"

        main_clip_name = file_utils.get_base_file_name_from(videofilepath)
        full_main_clip_file_path = videofilepath

        moviepy_utils.init_og_clip_params(full_main_clip_file_path)




        boomers_top, boomers_mid, boomers_bot = bu.filterBoomers(
            og_clip_duration= moviepy_utils.get_og_clip_params().get("duration"),
            boomers= boomers
        )

        params = ffmpeg_utils.buildCall(
            main_clip_name + ".mp4",
            boomers_bot + boomers_mid + boomers_top,
            ephemeral                        
        )

        for p in params :
            print(p, end= "\n\n")

        ffmpeg_utils.executeFfmpegCall(
            params= params
        )    




def is_audio_descriptor_call(videofilepath= None) :
    return True if (videofilepath) else False



def is_video_editor_call(videofilepath= None, boomers= None) :
    return True if (videofilepath and boomers is not None) else False

























































async def main() :
    videofilepath = sys.argv[1] if len(sys.argv) > 1 else None
    jsonfilepath = sys.argv[2] if len(sys.argv) > 2 else None
    sojufile= bu.get_sojufile_from_path(jsonfilepath)

    boomers = bu.get_boomers_from_dict(sojufile)
    
    if is_video_editor_call(videofilepath, boomers) :
        print("wait a moment...")
        video_editor(videofilepath, boomers)

    elif is_audio_descriptor_call(videofilepath) :
        print("wait a second...")
        await audio_descriptor(videofilepath, sojufile)










if __name__ == "__main__":
    asyncio.run(main())

