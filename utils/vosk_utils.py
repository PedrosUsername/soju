import wave
import json
import random

from vosk import Model, KaldiRecognizer

from . import boomer_utils as bu, file_utils as fu, moviepy_utils as mu
from .enum.Enum import ImageFilesDir, VideoFilesDir, AudioFilesDir
from .settings import constants







INTERVAL_DIFF_NOVOSK_DESCRIBE = constants.INTERVAL_DIFF_NOVOSK_DESCRIBE















def get_boomers_without_vosk(
        audio_file_path= None,
        image_files= [],
        audio_files= [],
        video_files= [],
        generator= {}       
    ) :
    if not audio_file_path :
        return []
    
    default_boomer = generator.get("defaults") if generator.get("defaults") else {}
    g_boomers = []
    og_clip_duration = mu.AudioFileClip( audio_file_path ).duration

    if og_clip_duration < 1 :
        return []
    
    qtd_boomers = int(og_clip_duration / INTERVAL_DIFF_NOVOSK_DESCRIBE) if og_clip_duration >= INTERVAL_DIFF_NOVOSK_DESCRIBE else 1

    tmp_clip_duration = og_clip_duration
    interval_start = 1
    interval_diffrence = INTERVAL_DIFF_NOVOSK_DESCRIBE if og_clip_duration >= INTERVAL_DIFF_NOVOSK_DESCRIBE else int(og_clip_duration)
    interval_end = interval_diffrence
    
    for _ in range(qtd_boomers) :
        word = default_boomer.get("word") if default_boomer.get("word") else {}
        word["start"] = random.choice(range(interval_start, interval_end))
        word["end"] = word["start"]

        g_boomer = bu.buildBoomer(
            obj= {
                "word": word.get("content"),
                "start": word["start"],
                "end": word["end"],
            },
            image_file_dirs= image_files,
            audio_file_dirs= audio_files,
            video_file_dirs= video_files,
            generator= generator
        )

        tmp_clip_duration = tmp_clip_duration - interval_diffrence
        interval_start = interval_end
        interval_diffrence = INTERVAL_DIFF_NOVOSK_DESCRIBE if tmp_clip_duration >= INTERVAL_DIFF_NOVOSK_DESCRIBE else int(tmp_clip_duration)
        interval_end = interval_end + interval_diffrence

        g_boomers.append(g_boomer)

    return g_boomers












def get_boomers_with_vosk(
        audio_file_path= None,
        image_files= [],
        audio_files= [],
        video_files= [],
        generator= {}            
    ) :
        if not audio_file_path :
            return []

        g_boomers = []
        model = Model(constants.PATH_MODEL)
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

        for sentence in results:
            if len(sentence) == 1:
                # sometimes there are bugs in recognition
                # and it returns an empty dictionary
                # {'text': ''}
                continue

            for obj in sentence['result']:
                g_boomer = bu.buildBoomer(
                    obj,
                    image_files,
                    audio_files,
                    video_files,
                    generator
                )

                g_boomers.append(g_boomer)

        wf.close()

        return g_boomers



























async def describe(audio_file_path= "", generator= {}, client= None) :
    generator_general_confs = generator.get("generals") if generator.get("generals") else {}
    default_boomer_structure = generator.get("defaults") if generator.get("defaults") else {}
    print(json.dumps(default_boomer_structure, indent= 4))

    valid_image_files_by_dir = {}
    valid_audio_files_by_dir = {}
    valid_video_files_by_dir = {}

    if default_boomer_structure.get("image") :
        for img_param in default_boomer_structure.get("image") :
            img_param_dir = bu.getBoomerImageParamDirForSojufile(img_param)

            if img_param_dir not in list(valid_image_files_by_dir.keys()) :
                if isinstance(img_param_dir, str) :
                    valid_image_files = fu.getValidImageFiles(ImageFilesDir.get( img_param_dir ))
                elif client and isinstance(img_param_dir, int) :
                    valid_image_files, aud, vid = await fu.getValidMediaFilesFromDiscordByChannelId(img_param_dir, client)
                else :
                    valid_image_files = []

                valid_image_files_by_dir.update({
                    img_param_dir: valid_image_files
                })

    if default_boomer_structure.get("audio") :
        for aud_param in default_boomer_structure.get("audio") :
            aud_param_dir = bu.getBoomerAudioParamDirForSojufile(aud_param)

            if aud_param_dir not in list(valid_audio_files_by_dir.keys()) :
                if isinstance(aud_param_dir, str) :
                    valid_audio_files = fu.getValidAudioFiles(AudioFilesDir.get( aud_param_dir ))
                elif client and isinstance(aud_param_dir, int) :
                    img, valid_audio_files, vid = await fu.getValidMediaFilesFromDiscordByChannelId(aud_param_dir, client)
                else :
                    valid_audio_files = []

                valid_audio_files_by_dir.update({
                    aud_param_dir: valid_audio_files
                })

    if default_boomer_structure.get("video") :
        for vid_param in default_boomer_structure.get("video") :
            vid_param_dir = bu.getBoomerVideoParamDirForSojufile(vid_param)

            if vid_param_dir not in list(valid_video_files_by_dir.keys()) :
                if isinstance(vid_param_dir, str) :
                    valid_video_files = fu.getValidVideoFiles(VideoFilesDir.get( vid_param_dir ))
                elif client and isinstance(vid_param_dir, int) :
                    img, aud, valid_video_files = await fu.getValidMediaFilesFromDiscordByChannelId(vid_param_dir, client)
                else :
                    valid_video_files = []

                valid_video_files_by_dir.update({
                    vid_param_dir: valid_video_files
                })


    g_boomers = []
    if (
        generator_general_confs.get("randomtimestamps")
    )  :
        g_boomers = get_boomers_without_vosk(
            audio_file_path= audio_file_path,
            image_files= valid_image_files_by_dir,
            audio_files= valid_audio_files_by_dir,
            video_files= valid_video_files_by_dir,
            generator= generator            
        )

    else :
        g_boomers = get_boomers_with_vosk(
            audio_file_path= audio_file_path,
            image_files= valid_image_files_by_dir,
            audio_files= valid_audio_files_by_dir,
            video_files= valid_video_files_by_dir,
            generator= generator
        )

    return g_boomers
