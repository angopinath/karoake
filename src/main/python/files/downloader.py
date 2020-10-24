import logging as log
import re

import music.music_meta as music_meta
import sites.web_scraper as scraper
import config
from files import file_utils


def download_from_url(url:str, path:str) -> music_meta.MusicMeta:
    log.debug("download started for the url {}".format(url))
    req = scraper.get_page(url)
    d = req.headers['content-disposition']
    name = re.findall('filename=(.+)', d)[0]
    name = name.replace(config.MUSIC_FILE_FORMAT, '')
    name = re.sub(r"[^a-zA-Z0-9]+", '_', name)
    name = name + config.MUSIC_FILE_FORMAT
    file_name = file_utils.form_path([path, name])
    with open(file_name,'wb') as f:
        f.write(req.content)
    log.debug('song has been downloaded {}'.format(file_name))
    return music_meta.get_music_meta(file_name)


def download_songs(urls:list, path:str) -> tuple:
    downloaded_songs = []
    non_downloaded_songs = []
    for song_url in urls:
        try:
            downloaded_songs.append(download_from_url(song_url, path))
        except Exception:
            log.exception('Exception while downloading song from {}'.format(song_url))
            non_downloaded_songs.append(song_url)
    return downloaded_songs, non_downloaded_songs

