import plistlib, sys, os

def main():

    xmlpath = 'itl.xml'
    print('Reading xml file ...')
    # xml = plistlib.readPlist(xmlpath)
    xml = plistlib.load(open(xmlpath, 'rb'))
    print('Reading tracks ...')
    tracks = xml['Tracks']
    print('Reading playlists ... ')
    playlists = xml['Playlists']
    print('Start!')

    folders = dict()
    root = list()
    for p in playlists:
        dirname = p.get('Parent Persistent ID')
        if dirname == None:
            root.append(p)
        else:
            if folders.get(dirname) == None:
                folders[dirname] = list()
            folders[dirname].append(p)
        names = list()
        for rootitem in root:
            if folders.get(rootitem['Playlist Persistent ID']) != None:
                folders[rootitem['Name']] = folders[rootitem['Playlist Persistent ID']]
                names.append(rootitem['Name'])
        for f in list(folders):
            if f not in names:
                del folders[f]

        names.extend(
            {
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
            })

        root = [p for p in root if p['Name'] not in names]

        rootpath = 'plsv2/'
        os.makedirs(rootpath, exist_ok=True)
        for p in root:
            p['Name'] = unix_name(p['Name'])
            print('|-', p['Name'])
            writepls(p, rootpath, tracks)
        for f in folders:
            print('|-', f)
            ppath = rootpath + unix_name(f) + '/'
            os.makedirs(ppath)
            for p in folders[f]:
                p['Name'] = unix_name(p['Name'])
                print('|--', p['Name'])
                writepls(p, ppath, tracks)

def unix_name(s):
    s = ''.join(e for e in s if e.isalnum() or e == ' ')
    s = s.replace(' ', '_')
    return s


def writepls(p, ppath, tracks):
    with open(ppath + p['Name'] + '.m3u', 'w+') as f:
        f.write('#EXTM3U\n')
        for t in p.get('Playlist Items', list()):
            tid = str(t['Track ID'])
            length = 0
            try:
                length = tracks[tid]['Total Time'] / 1000
            except Exception as e:
                print('LENGTH ERROR', tracks[tid]['Location'])
                artist = tracks[tid].get('Artist', '')
                name = tracks[tid].get('Name', '')
                location = tracks[tid]['Location']
                location = location.replace('localhost/C:/Users/Gebruiker', '/home/user1')
                f.write('#EXTINF:' + str(length) + ',' + artist + ' - ' + name + '\n')
                f.write(location + '\n')

if __name__ == '__main__':
    main()
