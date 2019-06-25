import plistlib, pickle, sys, os, anytree, urllib.parse
from anytree import Node, RenderTree
#  from itunes_smartplaylist import SmartPlaylistParser

fixed_names =\
[
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

    dict_by_id = dict()
    for p in playlists:
        dict_by_id[p.get("Playlist Persistent ID")] = (p, list())

    root = list()
    for p in playlists:
        parent = p.get("Parent Persistent ID")
        if parent is not None:
            dict_by_id[parent][1].append(p)

    total = 0
    for k in dict_by_id:
        p = dict_by_id[k]
        if len(p[1]) > 0 and p[0].get("Smart Info") is None: 
            #  print("Playlists: ", path)
            total += len(p[0].get('Playlist Items', list()))

    print(total)

if __name__ == '__main__':
    main()
