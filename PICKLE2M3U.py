import plistlib, pickle, sys, os


def main():
    print("Reading pickle")
    itl = pickle.load(open('itl.p', 'rb'))
    #  for t in itl['Tracks']:
    #      print(itl['Tracks'][t]['Name'])
    #  xmlpath = '/home/user1/Music/iTunes/iTunes Music Library.xml'
    #  print('Reading xml file ...')
    #  xml = plistlib.readPlist(xmlpath)
    print('Reading tracks ...')
    tracks = itl['Tracks']
    print('Reading playlists ... ')
    playlists = itl['Playlists']
    print('Start!')

    folders = dict()
    root = list()
    for p in playlists:
        dirname = p.get('Parent Persistent ID')
        if dirname == None:
            root.append(p)
        else:
            if folders.get(dirname) is  None:
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

    fixed_names.extend(
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

    root = [p for p in root if p['Name'] not in fixed_names]

    rootpath = 'pls/'
    os.makedirs(rootpath)
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
