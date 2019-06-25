import os

music_inodes = dict()
pls_inodes = dict()
lib_root = os.environ["HOME"] + "/Documents/itl/testenv/"

def main():
    for root, dirs, files in os.walk(lib_root + "music/", topdown=False):
        for name in files:
            path = os.path.join(root, name)
            music_inodes[os.stat(path)[1]] = path

    for root, dirs, files in os.walk(lib_root + "playlists/", topdown=False):
        for name in files:
            path = os.path.join(root, name)
            pls_inodes[os.stat(path)[1]] = path

    print("New files:")
    for new in set(pls_inodes.keys()) - set(music_inodes.keys()):
        format_copy(new)
        print(pls_inodes[new])

def format_copy(new):
    location = pls_inodes[new]
    path = lib_root + "music/"
    os.link(location, path + os.path.basename(location))

if __name__ == '__main__':
    main()
