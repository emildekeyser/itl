import plistlib, pickle

def load():
	itl = pickle.load(open('itl.p', 'rb'))
	for t in itl['Tracks']:
		print(itl['Tracks'][t]['Name'])

load()
