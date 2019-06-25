#!/home/user1/miniconda3/bin/python

import argparse
import plistlib
import sqlite3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--library',
                        help='Path to XML library file',
                        type=argparse.FileType('rb'),
                        default='./Library.xml')
    parser.add_argument('--db',
                        help='Path to SQLite DB file',
                        type=argparse.FileType('w+b'),
                        default='itunes.db')

    args = parser.parse_args()
    library = plistlib.load(args.library)

    tracks_table = process_tracks(library)
    playlists_table, playlist_itms_table = process_playlists(library)

    conn = sqlite3.connect(args.db)
    conn.execute(tracks_table)
    conn.execute(playlists_table)
    conn.execute(playlist_itms_table)

    conn.commit()
    conn.close()


def process_tracks(library):
    query = "INSERT INTO `CoreTracks` (TrackID,Uri,MimeType,FileSize,BitRate,SampleRate,Title,TitleLowered,TitleSort,TitleSortKey,TrackNumber,TrackCount,Disc,DiscCount,Duration,Year,Genre,Composer,Conductor,Grouping,Copyright,LicenseUri,Comment,Rating,Score,PlayCount,SkipCount,LastPlayedStamp,LastSkippedStamp,DateAddedStamp,DateUpdatedStamp,MetadataHash,BPM,LastSyncedStamp,FileModifiedStamp) "
    query += "VALUES "

    for track_id in library['Tracks'].keys():
        
        print(track_id)
        track = library['Tracks'][track_id]

        query += "("
        query += track['Track ID'] + ", "
        query += track['Location'] + ", "
        query += track['Kind'] + ", "
        query += track['Size'] + ", "
        query += track['Bit Rate'] + ", "
        query += track['Sample Rate'] + ", "
        query += track['Name'] + ", "
        query += track['Name'].lower() + ", "
        query += track['Total Time'] + ", "
        query += track['Track Number'] + ", "
        query += track['Year'] + ", "
        query += track['Date Modified'] + ", "
        query += track['Date Added'] + ", "
        query += track['Artwork Count'] + ", "
        query += track['Persistent ID'] + ", "
        query += track['Track Type'] + ", "
        query += track['File Folder Count'] + ", "
        query += track['Library Folder Count'] + ", "
        query += track['Artist'] + ", "
        query += track['Album'] + ", "
        query += track['Genre'] + ", "
        query += track['Comments'] + ", "
        query += "),"

    return query


def process_playlists(library):
    all_keys = set()
    inserts = []

    for playlist in library['Playlists']:
        print(playlist)
        try:
            track_ids = playlist['Playlist Items']
            del playlist['Playlist Items']
        except KeyError as e:
            track_ids = []

        playlist_keys = list(map(slugify, playlist.keys()))
        playlist_values = playlist.values()

        all_keys = all_keys.union(set(playlist_keys))

        inserts.append(get_parameterized(
            'playlists', playlist_keys, playlist_values)
        )

        for track in track_ids:
            inserts.append(get_parameterized(
                'playlist_items',
                ['playlist_id', 'track_id'],
                [playlist['Playlist ID'], track['Track ID']]
            ))

    playlists_table = "CREATE TABLE playlists ({0})".format(
        ', '.join(all_keys)
    )
    items_table = 'CREATE TABLE playlist_items (playlist_id, track_id)'

    return playlists_table, items_table, inserts


if __name__ == '__main__':
    main()