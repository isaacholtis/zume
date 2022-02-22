import os, sys
from tinytag import TinyTag

path = 'D:/Music/'
bigList = {}


for root, dirs, files in os.walk(path):
	for file in files:
		#append the file name to the list
		ext = os.path.splitext(file)[1]

		if ext == ".mp3" or ext == ".wav" or ext == ".flac" or ext == ".ogg" or ext == ".mp3" or ext == ".mp3": #wma not supported by pygame mixer
			tag = TinyTag.get(os.path.join(root,file), image=True)
			artist = tag.albumartist
			album = tag.album
			track = tag.track
			title = tag.title
			song = tag.title
			path = os.path.join(root,file)
			if artist in bigList:
				pass
			else:	
				bigList[artist] = {}

			if album in bigList[artist]:
				pass
			else:
				bigList[artist][album] = []

			bigList[artist][album].append([track, title, path]) #hmmmmm nope



for album in bigList[artist][album]:
	album.sort() 

print(bigList)



sys.exit()