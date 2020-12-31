#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv


def enumerate_playlists(root):
    if not os.path.isdir(root):
        raise Exception()
    for dn in os.listdir(root):
        playlist_path = os.path.join(root, dn)
        if not os.path.isdir(playlist_path):
            continue
        print(playlist_path)
        tracks = list(enumerate_tracks(playlist_path))
        tracks.sort(key=lambda x: x[7])  # sorted by `index in the playlist`
        print((dn, tracks))
        yield dn, tracks


def enumerate_tracks(playlist_path):
    track_path = playlist_path
    if not playlist_path.endswith('高く評価した曲'):
        track_path = os.path.join(playlist_path, 'トラック')
    for fn in os.listdir(track_path):
        metadata_path = os.path.join(track_path, fn)
        if not os.path.isfile(metadata_path):
            continue
        meta = parse_metadata(metadata_path)
        yield meta


def parse_metadata(metadata_path):
    with open(metadata_path, encoding='utf-8') as f:
        r = csv.reader(f)
        header = next(r)
        res = next(r)
        return res


def main():
    list(enumerate_playlists(r'path_to_your\Takeout\Google Play Music\プレイリスト'))


if __name__ == '__main__':
    main()
