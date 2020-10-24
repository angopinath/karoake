import music_tag
import config
import json
import collections


MusicMeta = collections.namedtuple('MusicMeta', ['path', 'title', 'album', 'composer', 'artist'])


def get_music_meta(file: str) -> MusicMeta:
    tag_file = music_tag.load_file(file)
    return create_meta(file, remove_blacklist(str(tag_file['title'])), str(tag_file['album']), remove_blacklist(str(tag_file['composer'])), remove_blacklist(str(tag_file['artist'])))


def get_music_meta_list(files: list) -> list:
    return [get_music_meta(file) for file in files]


def create_music_meta(file: str, meta: MusicMeta) -> MusicMeta:
    tag_file = music_tag.load_file(file)
    tag_file['title'] = meta.title
    tag_file['album'] = meta.album
    tag_file['composer'] = meta.composer
    tag_file['artist'] = meta.artist
    tag_file.save()
    return modify_path_from_meta(file, meta)


def modify_path_from_meta(file, meta: MusicMeta) -> MusicMeta:
    return create_meta(file, meta.title, meta.album, meta.composer, meta.artist)


def create_meta(file, title, album, composer, artist) -> MusicMeta:
    return MusicMeta(file, title, album, composer, artist)


def remove_blacklist(name) -> str:
    for blacklist in config.BLACK_LIST_META:
        name = name.replace(blacklist, '')
    return name


def save_meta(meta: MusicMeta) -> MusicMeta:
    json_dump = json.dumps(meta._asdict())
    file_name = meta.path + config.META_SUFFIX
    with open(file_name,'w+') as f:
        f.write(json_dump)
    return meta


def load_meta(file: str) -> MusicMeta:
    f = open(file, 'r')
    meta = MusicMeta(**json.loads(f.read()))
    f.close()
    return meta


if __name__ == '__main__':
    meta = get_music_meta('/tmp/sadsongs1/download/Alwa Nayagan.mp3')
    save_meta(meta)
    meta2 = load_meta('/tmp/sadsongs1/download/Alwa Nayagan.mp3.meta')
    print(meta2)

