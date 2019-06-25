import os
from fuzzywuzzy import process


a = set()
r = "/home/user1/Music/iTunes/iTunes Media/Music/" 
for root, dirs, files in os.walk(r, topdown=False):
    for name in files:
        a.add(os.path.join(root, name))
        print(name)

to_find = "/home/user1/Music/iTunes/iTunes Media/Music/Salut C'est Cool/Reprises/13 Quelqu'un de bien (Enzo Enzo).mp3"

result = process.extractOne(to_find, a)

print(result)

to_find = "/home/user1/Music/iTunes/iTunes Media/Music/Salut C'est Cool/Reprises/12 The fool on the hill (The Beatles.mp3"
result = process.extractOne(to_find, a)
print(result)
