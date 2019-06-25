import plistlib, pickle, sys, os, urllib.parse
from fuzzywuzzy import process

libpath = os.environ["HOME"] + "/music/library/pls/"

all_songs = set()
music_root = os.environ["HOME"] + "/music/iTunes/iTunes Media/Music/" 
for root, dirs, files in os.walk(music_root, topdown=False):
    for name in files:
        all_songs.add(os.path.join(root, name))
all_songs = list(all_songs)

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
    # print("Reading pickle")
    # itl = pickle.load(open('itl.p', 'rb'))
    #  for t in itl['Tracks']:
    #      print(itl['Tracks'][t]['Name'])
    xmlpath = os.environ['HOME'] + '/quest/itl/itl.xml'
    print('Reading xml file ...')
    # itl = plistlib.readPlist(xmlpath)
    itl = plistlib.load(open(xmlpath, 'rb'))
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

    for k in dict_by_id:
        p = dict_by_id[k]
        if p[0]["Name"] not in fixed_names:
            path = ""
            parent = p[0].get("Parent Persistent ID")
            while parent is not None:
                path = unix_name(dict_by_id[parent][0]["Name"]) + "/" + path
                parent = dict_by_id[parent][0].get("Parent Persistent ID")
            path = libpath + path + "/"
            name = unix_name(p[0]["Name"]) + "/"
            if p[0].get("Smart Info") is not None: 
                name = "00." + name
            path += name
            path = path.replace("//", "/")
            try:
                os.makedirs(path)
            except:
                print("ERROR %s exists" % path)
            if len(p[1]) > 0:
                print("Folder: ", path)
            elif p[0].get("Smart Info") is None:
                print("Playlists: ", path)
                make_playlist(path, p[0], tracks)
            else:
                print("smart: ", path)
    return 0

def make_playlist(path, p, tracks):
    for t in p.get('Playlist Items', list()):
        tid = str(t['Track ID'])
        location = actual_location(tracks[tid]['Location'])
        try:
            os.link(location, path + os.path.basename(location))
        except Exception as e:
            #  print("ERROR with link %s" % location)
            print(e)

def actual_location(location):
    location = location.replace('file://localhost/C:/Users/Gebruiker', '/home/user1')
    location = urllib.parse.urlparse(location).path
    location = urllib.parse.unquote(location)
    return process.extractOne(location, all_songs)[0]

def unix_name(s):
    s = ''.join(e for e in s if e.isalnum() or e == ' ')
    s = s.replace(' ', '_')
    return s

if __name__ == '__main__':
    main()
