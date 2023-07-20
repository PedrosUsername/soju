import asyncio
import sys

import cli as soju



MAKEITREAL_GENERATOR_PATH = "./assets/json/makeitreal.soju.json"



async def makeitreal() :
    videofilepath = sys.argv[1] if len(sys.argv) > 1 else None
    jsonfilepath = MAKEITREAL_GENERATOR_PATH
    dropzone = "./"

    sojufile= soju.bu.get_sojufile_from_path(jsonfilepath)
    boomers = soju.bu.get_boomers_from_dict(sojufile)
    generator = soju.bu.prepare_boomer_generator(soju.bu.get_boomer_generator_from_dict(sojufile))

    generator["generals"]["dropzone"] = dropzone

    print("wait a second...")
    await soju.audio_descriptor(videofilepath, generator)

    new_sojufile = soju.bu.get_sojufile_from_path(dropzone + soju.file_utils.get_base_file_name_from(videofilepath) + ".soju.json")
    boomers = new_sojufile.get("generated") if new_sojufile.get("generated") else []

    print("wait a moment...")
    soju.video_editor(videofilepath, generator, boomers)




asyncio.run(makeitreal())