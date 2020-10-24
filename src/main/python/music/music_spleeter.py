from spleeter.separator import Separator
import os

import config
from music import music_meta
import files.file_utils as file_utils


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class Spleeter:

    def __init__(self):
        self.music_format = config.MUSIC_FILE_FORMAT.replace('.', '')
        self.separater = Separator('spleeter:2stems')
        self.musics = []

    def split_music(self, path: str, audio_file: music_meta.MusicMeta = None, audio_files: list = None):
        files = Spleeter.__get_files__(audio_file, audio_files)
        path = file_utils.create_path([path])
        moved_path = file_utils.create_path([path, config.LOCATION_SPLEETER_MOVED])
        for file in files:
            self.separater.separate_to_file(audio_descriptor=file.path, destination=path, codec=self.music_format, filename_format='{instrument}/{filename}.{codec}')
            file_name = file_utils.extract_file_name_from_path(file.path)
            music_file_name = Spleeter.__get_music_path__(path, file_name)
            self.musics.append(music_meta.create_music_meta(music_file_name, file))
            file_utils.move_file(file.path, moved_path)

    @staticmethod
    def __get_files__(audio_file, audio_files):
        files = []
        if audio_file:
            files.append(audio_file)
        if audio_files:
            files.extend(audio_files)
        if not files:
            raise Exception('either audio_file or audio_files should be provided')
        return files

    @staticmethod
    def __get_music_path__(path:str, name:str) -> str:
        return file_utils.form_path([path, config.INSTRUMENT_MUSIC, name + config.MUSIC_FILE_FORMAT])
