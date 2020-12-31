#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import taglib


def enumerate_tracks(root):
    if not os.path.isdir(root):
        raise Exception()
    for fn in os.listdir(root):
        try:
            mp3_path = os.path.join(root, fn)
            if not os.path.isfile(mp3_path) or not mp3_path.endswith(".mp3"):
                continue
            meta = parse_metadata(mp3_path)
            print(meta)
            yield meta
        except OSError:
            pass


def parse_metadata(mp3_path):
    song = taglib.File(mp3_path)
    meta = dict()
    meta['title'] = song.tags['TITLE'][0] if 'TITLE' in song.tags else ''
    meta['album'] = song.tags['ALBUM'][0] if 'ALBUM' in song.tags else ''
    meta['artist'] = song.tags['ARTIST'][0] if 'ARTIST' in song.tags else ''
    return mp3_path, meta


def main():
    list(enumerate_tracks(r'path_to_your\Takeout\Google Play Music\トラック'))


if __name__ == '__main__':
    main()
