from files import file_utils
from music.music_spleeter import Spleeter
import music.music_converter as mp4convertor
import music.music_meta as music_meta
import files.downloader as downloader
import youtube.upload as youtube_uploader
from sites import ScraperSiteOpt
import config

import logging as log
import argparse
from enum import Enum

log.basicConfig(format='%(asctime)s : %(levelname)s : %(funcName)s : %(lineno)d :: %(message)s', level = log.DEBUG)


class Operation(Enum):
    FULL = 'FULL',
    CREATOR = 'CREATOR',
    SCRAP_PAGE = 'SCRAP_PAGE',
    SCRAP_ALL_PAGE = 'SCRAP_ALL_PAGE',
    DOWNLOAD = 'DOWNLOAD',
    DOWNLOAD_LIST = 'DOWNLOAD_LIST',
    SPLEETER = 'SPLEETER',
    SPLEETER_LIST = 'SPLEETER_LIST',
    CONVERT = 'CONVERT',
    CONVERT_LIST = 'CONVERT_LIST',
    UPLOAD = 'UPLOAD',
    UPLOAD_LIST = 'UPLOAD_LIST'

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    @staticmethod
    def argparse(s):
        try:
            return Operation[s]
        except KeyError:
            return s


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--operation', required=True, type=Operation.argparse, help='give operation type', choices=list(Operation))
    parser.add_argument('-in', '--input', help='given input', required=True)
    parser.add_argument('-out', '--output_path', required=True, help='give output path')
    return parser


def main():
    args = get_arg_parser().parse_args()
    args.operation = Operation(args.operation)

    if Operation.FULL == args.operation:
        scraper_site = ScraperSiteOpt.__get_scraper_site__(args.input)
        scraper_site.find_all_songs()
        scraper_site.export(file_utils.form_path([args.output_path, config.LOCATION_URL_FILE_NAME]))
        download_path = file_utils.create_path([args.output_path, config.LOCATION_DOWNLOAD])
        song_list, url_list = downloader.download_songs(scraper_site.downloadables, download_path)
        if url_list:
            log.error('there is non downloaded songs. pls check {}'.format(args.output_path))
            file_utils.save_list(url_list, file_utils.form_path([args.output_path, config.LOCATION_URL_FILE_NAME]))
        spleeter = Spleeter()
        spleeter.split_music(args.output_path, audio_files=song_list)
        video_list = mp4convertor.convert_list(spleeter.musics, args.output_path)
        log.info("all operation as been completed")
        log.info((video_list))

    elif Operation.CREATOR == args.operation:
        spleeter = Spleeter()
        song_list = file_utils.get_music_files(args.input)
        spleeter.split_music(args.output_path, audio_files=song_list)
        video_list = mp4convertor.convert_list(spleeter.musics, args.output_path)
        log.info("all operation as been completed")
        log.info((video_list))

    elif Operation.SCRAP_PAGE == args.operation:
        scraper_site = ScraperSiteOpt.__get_scraper_site__(args.input)
        scraper_site.find_songs()
        scraper_site.export(file_utils.form_path([args.output_path, config.LOCATION_URL_FILE_NAME]))

    elif Operation.SCRAP_ALL_PAGE == args.operation:
        scraper_site = ScraperSiteOpt.__get_scraper_site__(args.input)
        scraper_site.find_all_songs()
        scraper_site.export(file_utils.form_path([args.output_path, config.LOCATION_URL_FILE_NAME]))

    elif Operation.DOWNLOAD == args.operation:
        songs_location = downloader.download_from_url(args.input, args.output_path)
        log.info(songs_location)

    elif Operation.DOWNLOAD_LIST == args.operation:
        song_url_list = file_utils.get_songs_from_file(args.input)
        download_path = file_utils.create_path([args.output_path, config.LOCATION_DOWNLOAD])
        song_list, url_list = downloader.download_songs(song_url_list, download_path)
        if url_list:
            log.error('there is non downloaded songs. pls check {}'.format(args.output_path))
            file_utils.save_list(url_list, file_utils.form_path([args.output_path, config.LOCATION_URL_FILE_NAME]))

    elif Operation.SPLEETER == args.operation:
        song = music_meta.get_music_meta(args.input)
        spleeter = Spleeter()
        music = spleeter.split_music(args.output_path, song)
        log.info(music)

    elif Operation.SPLEETER_LIST == args.operation:
        song_list = file_utils.get_music_files(args.input)
        spleeter = Spleeter()
        music_list = spleeter.split_music(args.output_path, audio_files=song_list)
        log.info(music_list)

    elif Operation.CONVERT == args.operation:
        music = music_meta.get_music_meta(args.input)
        video = mp4convertor.convert(music, args.output_path)
        log.info(video)

    elif Operation.CONVERT_LIST == args.operation:
        music_list = file_utils.get_music_files(args.input)
        videos = mp4convertor.convert_list(music_list, args.output_path)
        log.info(videos)

    elif Operation.UPLOAD == args.operation:
        youtube = youtube_uploader.get_authenticated_service()
        video_meta = music_meta.load_meta(args.input)
        youtube_uploader.initialize_upload(youtube, video_meta)

    elif Operation.UPLOAD_LIST == args.operation:
        youtube = youtube_uploader.get_authenticated_service()
        videos_meta = file_utils.get_music_list_from_meta_files(args.input)
        youtube_uploader.upload_list(youtube, videos_meta, args.output_path)


if __name__ == '__main__':
    main()

