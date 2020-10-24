import shutil
import os
import logging as log
import glob
import ntpath

import config
from music.music_meta import MusicMeta, get_music_meta_list, load_meta


def save_list(vals, file):
    with open(file, 'w+') as f:
        for item in vals:
            f.write("%s\n" % item)
    log.info("songs download url has been scraped in {} file".format(file))


def get_songs_from_file(file:str) -> list:
    return open(file).readlines()


def move_file(file:str, path: str):
    shutil.move(file, path)


def get_music_files(path:str) -> list:
    filenames = glob.glob(os.path.join(path, '*' + config.MUSIC_FILE_FORMAT))
    return get_music_meta_list(filenames)


def get_music_list_from_meta_files(path:str) -> list:
    filenames = glob.glob(os.path.join(path, '*' + config.META_SUFFIX))
    return [load_meta(file) for file in filenames]


def create_path(args):
    path = form_path(args)
    os.makedirs(path, exist_ok=True)
    return path


def form_path(args) -> str:
    return os.path.join(*args)


def extract_file_name_from_path(path:str) -> str:
    return ntpath.splitext(ntpath.basename(path))[0]


def save_tpl(meta: MusicMeta):
    content = open(config.TPL_SAMPLE_FILE, 'r').read()
    content = content.replace(config.TPL_TITLE_PLACEHOLDER, create_title(meta))
    content = content.replace(config.TPL_DESC_PLACEHOLDER, create_desc(meta))
    content = content.replace(config.TPL_TAGS_PLACEHOLDER, ','.join(create_tags(meta)))
    tpl_file = meta.path.replace(config.VIDEO_FILE_FORMAT, config.TPL_SUFFIX)
    open(tpl_file, 'w+').write(content)


def create_title(file_meta: MusicMeta):
    return ' | '.join([file_meta.title, file_meta.album, file_meta.composer, file_meta.artist, config.YOUTUBE_DESC])


def get_hashtag(file_meta: MusicMeta) -> str:
    return '#{} #{}, #{}'.format(config.YOUTUBE_DESC.replace(' ', ''), file_meta.title.replace(' ',''), file_meta.composer.replace(' ', ''))


def create_desc(file_meta: MusicMeta):
    return 'title: {}\nalbum: {}\ncomposer: {}\nartist: {}\n{}'.format(file_meta.title, file_meta.album, file_meta.composer, file_meta.artist, get_hashtag(file_meta))


def create_tags(file_meta: MusicMeta):
    tag_list = [file_meta.title, file_meta.album, file_meta.composer]
    tag_list.extend(file_meta.artist.split())
    tag_list.extend(config.YOUTUBE_KEYWORDS)
    return tag_list

