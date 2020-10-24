import math
import logging as log
import random
import pandas as pd

import config
from music.music_meta import MusicMeta
from files import file_utils
import music.music_meta as music_meta
from moviepy.editor import *


def get_sample_video(time: int) -> VideoClip:
    video = VideoFileClip(random.choice(config.SAMPLE_VIDEO_FILES))
    video = video.subclip(config.SAMPLE_VIDEO_START_TIME, video.duration)
    videos = [video] * math.ceil(time/( video.duration - config.SAMPLE_VIDEO_START_TIME))
    video = concatenate_videoclips(videos)
    return video.set_duration(time)


def convert(meta:MusicMeta, path: str) -> MusicMeta:
    audiofile = AudioFileClip(filename=meta.path)
    videofile = get_sample_video(audiofile.duration)
    videofile = videofile.set_audio(audiofile)

    output_file_path = '.'.join([file_utils.extract_file_name_from_path(meta.path), 'mp4'])

    output_file = file_utils.form_path([path, output_file_path])
    new_meta = music_meta.modify_path_from_meta(output_file, meta)

    videofile.write_videofile(output_file)
    file_utils.save_tpl(new_meta)

    return new_meta


def convert_list(file_list:list, path:str) -> list:
    video_converted_path = file_utils.create_path([path, config.LOCATION_VIDEO_CONVERTED])
    video_moved_path = file_utils.create_path([path, config.LOCATION_VIDEO_MOVED])
    video_metas=[]
    for file in file_list:
        try:
            meta = convert(file, video_converted_path)
            file_utils.move_file(file.path, video_moved_path)
            video_metas.append(meta)
        except Exception as e:
            log.error('error while converting video from {}'.format(file.path))
            log.error(e)
    return video_metas


def cut(song: MusicMeta, limit: int):
    audiofile = AudioFileClip(filename=song.path)
    df = pd.DataFrame([], columns=['isVocal'])
    for i in range(int(audiofile.duration)):
        df.loc[i] = all(abs(f) >= 0.01000000 for f in audiofile.get_frame(i))
    df = df.rolling(5).max()
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(df)




if __name__ == '__main__':
    meta = music_meta.get_music_meta('/root/gerrit/karaoke/kaviya-thalivan/vocals/Yaarumilla.mp3')
    cut(meta, 10)