import asyncio
import sys

import cli as soju



MAKEITREAL_GENERATOR_PATH = "./assets/json/makeitreal.soju.json"



async def makeitreal() :
    videofilepath = sys.argv[1] if len(sys.argv) > 1 else None
    jsonfilepath = MAKEITREAL_GENERATOR_PATH

    sojufile = soju.bu.get_sojufile_from_path(jsonfilepath)

    print("wait a second...")
    await soju.audio_descriptor(videofilepath, sojufile)


    new_sojufile = soju.bu.get_sojufile_from_path(soju.file_utils.get_base_file_name_from(videofilepath) + ".soju.json")
    boomers = new_sojufile.get("generated") if new_sojufile.get("generated") else []

    print("wait a moment...")
    soju.video_editor(videofilepath, boomers)




asyncio.run(makeitreal())