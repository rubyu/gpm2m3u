#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import taglib


def enumerate_tracks(root):
    if not os.path.isdir(root):
        raise Exception()
    for root, dirs, files in os.walk(root):
        for file in files:
            try:
                flac_path = os.path.join(root, file)
                if not os.path.isfile(flac_path) or not flac_path.endswith(".flac"):
                    continue
                meta = parse_metadata(flac_path)
                print(meta)
                yield meta
            except OSError:
                pass


def parse_metadata(flac_path):
    song = taglib.File(flac_path)
    meta = dict()
    meta['title'] = song.tags['TITLE'][0] if 'TITLE' in song.tags else ''
    meta['album'] = song.tags['ALBUM'][0] if 'ALBUM' in song.tags else ''
    meta['artist'] = song.tags['ARTIST'][0] if 'ARTIST' in song.tags else ''
    return flac_path, meta


def main():
    list(enumerate_tracks(r'path_to_your_flac_library'))


if __name__ == '__main__':
    main()
