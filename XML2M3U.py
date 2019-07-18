import plistlib, sys, os, urllib.parse

EXCLUDED_PLAYLISTS = [
    '####!####',
    'Music',
    'Music Videos',
    'Rentals',
    'Films',
    'Home Videos',
    'TV Programmes',
    'Podcasts',
    'iTunes U',
    'Books',
    'Books',
    'PDFs',
    'Audiobooks',
    'Genius',
    'Play'
]
PATH_SEPARATOR = '==='

def load_itl():
    xmlpath = 'itl.xml'
    xml = plistlib.load(open(xmlpath, 'rb'))
    global TRACKS
    global PLAYLISTS
    TRACKS = xml['Tracks']
    PLAYLISTS = {}
    for p in xml['Playlists']:
        if p.get('Name') not in EXCLUDED_PLAYLISTS:
            PLAYLISTS[p.get('Playlist Persistent ID')] = p

def main():
    load_itl()
    for pid in PLAYLISTS:
        pls_path = with_parents(pid)
        print(pls_path)
        writepls(pls_path, pid)


def with_parents(pid):
    p = PLAYLISTS[pid]
    parent_pid = p.get('Parent Persistent ID')
    path = PATH_SEPARATOR + p.get('Name')
    if parent_pid != None:
        return with_parents(parent_pid) + path
    return path


    #     root = [p for p in root if p['Name'] not in names]

    #     rootpath = 'plsv2/'
    #     os.makedirs(rootpath, exist_ok=True)
    #     for p in root:
    #         p['Name'] = unix_name(p['Name'])
    #         print('|-', p['Name'])
    #         writepls(p, rootpath, tracks)
    #     for f in folders:
    #         print('|-', f)
    #         ppath = rootpath + unix_name(f) + '/'
    #         os.makedirs(ppath)
    #         for p in folders[f]:
    #             p['Name'] = unix_name(p['Name'])
    #             print('|--', p['Name'])
    #             writepls(p, ppath, tracks)

def unix_name(s):
    s = ''.join(e for e in s if e.isalnum() or e == ' ')
    s = s.replace(' ', '_')
    return s


def writepls(pls_path, pid):
    pls_tracks = PLAYLISTS[pid].get('Playlist Items', list())
    with open(pls_path + '.m3u', 'w+') as f:
        f.write('#EXTM3U\n')
        for t in pls_tracks:
            tid = str(t['Track ID'])
            length = 0
            try:
                length = TRACKS[tid]['Total Time'] / 1000
            except Exception as e:
                print('LENGTH ERROR', TRACKS[tid]['Location'])
            artist = TRACKS[tid].get('Artist', '')
            name = TRACKS[tid].get('Name', '')
            location = TRACKS[tid]['Location']
            location = location.replace('file://localhost/home/user1/Music/iTunes/iTunes%20Media/Music', '/data/music/library/artists')
            f.write('#EXTINF:' + str(length) + ',' + artist + ' - ' + name + '\n')
            f.write(urllib.parse.unquote(location) + '\n')

if __name__ == '__main__':
    main()
