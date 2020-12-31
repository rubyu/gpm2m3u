#!/usr/bin/env python
# -*- coding: utf-8 -*-


import mp3_track
import flac_track
import playlist

import os
from urllib.parse import urlencode, parse_qs
import html
import csv


def to_key_for_song(track_meta):
    return urlencode(track_meta)


def to_track_meta(row):
    d = {
        'title': html.unescape(row[0]),
        'album': html.unescape(row[1]),
        'artist': html.unescape(row[2]),
    }
    return d


def generate_song_dict(path):
    d = dict()
    for track_path, track_meta in mp3_track.enumerate_tracks(path):
        key_for_song = to_key_for_song(track_meta)
        d[key_for_song] = track_path
    return d


def update_song_dict(song_dict, path):
    d = song_dict.copy()
    for track_path, track_meta in flac_track.enumerate_tracks(path):
        key_for_song = to_key_for_song(track_meta)
        if key_for_song in d:
            print(f'Update {track_meta}')
        d[key_for_song] = track_path
    return d


def dump_song_dict(song_dict, path):
    with open(path, 'w', newline="", encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        for k, v in song_dict.items():
            d = parse_qs(k)
            print(d)
            writer.writerow([
                d['title'][0] if 'title' in d else '',
                d['album'][0] if 'album' in d else '',
                d['artist'][0] if 'artist' in d else '',
                v,
            ])


def export_m3u(path, tracks):
    m3u = '\r\n'.join(tracks)
    print(m3u)
    with open(path, 'w', newline="", encoding='utf-8') as f:
        f.write(m3u)


def main():
    # Output csv and m3u8 files under this directory.
    output_dir = r'output'

    # Set the path of your `Google Play Music` directory exported from GPM and extracted.
    gpm_takeout_dir = r'path_to_your\Takeout\Google Play Music'
    track_dir = os.path.join(gpm_takeout_dir, 'トラック')
    playlist_dir = os.path.join(gpm_takeout_dir, 'プレイリスト')

    # Set r'path_to_your_flac_library' if you need to update songs exported from GPM with flac files which have same
    # title, album, and artist.
    flac_dir = ''

    # Output this file instead of the real one if corresponding song is missing.
    # This can be happen in case you had modified tags on GPM's UI.
    notfound_mp3 = r'gpm2m3u_notfound.mp3'

    song_dict = generate_song_dict(track_dir)
    dump_song_dict(song_dict, os.path.join(output_dir, 'all_tracks.csv'))
    if flac_dir:
        song_dict = update_song_dict(song_dict, flac_dir)
        dump_song_dict(song_dict, os.path.join(output_dir, 'all_tracks_flac_merged.csv'))

    for playlist_name, playlist_meta in playlist.enumerate_playlists(playlist_dir):
        tracks = []
        for row in playlist_meta:
            key_for_song = to_key_for_song(to_track_meta(row))
            if key_for_song in song_dict:
                tracks.append(song_dict[key_for_song])
            else:
                print(f"Missing: {row}")
                tracks.append(f'# {row}')
                tracks.append(notfound_mp3)
        export_m3u(os.path.join(output_dir, f'{playlist_name}.m3u8'), tracks)


if __name__ == '__main__':
    main()
