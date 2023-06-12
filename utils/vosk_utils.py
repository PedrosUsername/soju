import wave
import json

from vosk import Model, KaldiRecognizer

from . import boomer_utils as bu, file_utils as fu
from .enum.Enum import ImageFilesDir, VideoFilesDir, AudioFilesDir
from .settings import variables
























async def describe(audio_file_path= "", generator= None, client= None) :
    generator = bu.prepare_boomer_generator(generator)
    default_boomer_structure = generator.get("defaults") if generator.get("defaults") else {}
    print(json.dumps(default_boomer_structure, indent= 4))

    valid_image_files_by_dir = {}
    valid_audio_files_by_dir = {}
    valid_video_files_by_dir = {}

    if default_boomer_structure.get("image") :
        for img_param in default_boomer_structure.get("image") :
            img_param_dir = bu.getBoomerImageParamDirForFFMPEG(img_param)

            if img_param_dir not in list(valid_image_files_by_dir.keys()) :
                if isinstance(img_param_dir, str) :
                    valid_image_files = fu.getValidImageFiles(ImageFilesDir.get( img_param_dir ))
                elif isinstance(img_param_dir, int) :
                    valid_image_files, aud, vid = await fu.getValidMediaFilesFromDiscordByChannelId(img_param_dir, client)
                else :
                    valid_image_files = []

                valid_image_files_by_dir.update({
                    img_param_dir: valid_image_files
                })

    if default_boomer_structure.get("audio") :
        for aud_param in default_boomer_structure.get("audio") :
            aud_param_dir = bu.getBoomerAudioParamDirForFFMPEG(aud_param)

            if aud_param_dir not in list(valid_audio_files_by_dir.keys()) :
                if isinstance(aud_param_dir, str) :
                    valid_audio_files = fu.getValidAudioFiles(AudioFilesDir.get( aud_param_dir ))
                elif isinstance(aud_param_dir, int) :
                    img, valid_audio_files, vid = await fu.getValidMediaFilesFromDiscordByChannelId(aud_param_dir, client)
                else :
                    valid_audio_files = []

                valid_audio_files_by_dir.update({
                    aud_param_dir: valid_audio_files
                })

    if default_boomer_structure.get("video") :
        for vid_param in default_boomer_structure.get("video") :
            vid_param_dir = bu.getBoomerVideoParamDirForFFMPEG(vid_param)

            if vid_param_dir not in list(valid_video_files_by_dir.keys()) :
                if isinstance(vid_param_dir, str) :
                    valid_video_files = fu.getValidVideoFiles(VideoFilesDir.get( vid_param_dir ))
                elif isinstance(vid_param_dir, int) :
                    img, aud, valid_video_files = await fu.getValidMediaFilesFromDiscordByChannelId(vid_param_dir, client)
                else :
                    valid_video_files = []

                valid_video_files_by_dir.update({
                    vid_param_dir: valid_video_files
                })

    model = Model(variables.PATH_MODEL)
    wf = wave.open(audio_file_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    # recognize speech using vosk model
    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)
    part_result = json.loads(rec.FinalResult())
    results.append(part_result)

    # convert list of JSON dictionaries to list of 'Word' objects
    word_list = []
    for sentence in results:
        if len(sentence) == 1:
            # sometimes there are bugs in recognition
            # and it returns an empty dictionary
            # {'text': ''}
            continue

        for obj in sentence['result']:
            new_word = bu.buildBoomer(
                obj,
                valid_image_files_by_dir,
                valid_audio_files_by_dir,
                valid_video_files_by_dir,
                default_boomer_structure
            )

            word_list.append(new_word)  # and add it to list

    wf.close()  # close audiofile
    return word_list
