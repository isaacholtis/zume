# This Python file uses the following encoding: utf-8
from tinytag import TinyTag #1.8.1 or later
import pygame
import os, io, time, random, sys, json
from operator import itemgetter

#initialise pygame and font ------------------------------------------------------------------
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.01)
pygame.key.set_repeat(200)
MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)
#---------------------------------------------------------------------------------------------

#font declarations ---------------------------------------------------------------------------
boldSmall = pygame.font.SysFont("Segoe UI", size = 15, bold = True)
regSmall = pygame.font.SysFont("Segoe UI", size = 15)

lrgFont = pygame.font.SysFont("Segoe UI", size = 45) 
medFont = pygame.font.SysFont("Segoe UI", size = 30)
smallFont = pygame.font.SysFont("Segoe UI", size = 18)
#---------------------------------------------------------------------------------------------

#make the window -----------------------------------------------------------------------------
WIN = pygame.display.set_mode((240, 320))
PYGAME_HIDE_SUPPORT_PROMPT=1
#Screen: 3 inches (7.62 cm) diagonal, 2.4 inches (0.610 cm) × 1.8 inches (0.457 mm) QVGA LCD, 320×240 pixels, 133.33 PPI, 65k colors (16-bit color)
pygame.display.set_icon(pygame.image.load(os.path.join('Assets', 'logo.png')))
pygame.display.set_caption("zume")
#---------------------------------------------------------------------------------------------

#colours -------------------------------------------------------------------------------------
ZumeGrey = (48, 46, 48)
ZumeLGrey = (105, 105, 105)
ZumeWhite = (255, 255, 255)
#---------------------------------------------------------------------------------------------

#weird variables------------------------------------------------------------------------------
tag = ''
albumArt = ''
clock = pygame.time.Clock()
FPS = 15
mainMenuCount = 0
subMenuCount = 0
musicMenuTop = 'songs'
#---------------------------------------------------------------------------------------------

#working with variables---------------------------------------------------------------------
f = open('mylib.json')
libraryList = json.load(f)
artistList = []
albumList = []
songList = []
for artist in libraryList:
	artistList.append([str(artist),""])
	for item in list(libraryList[artist].keys()):
		albumList.append([item,artist])
		for thesong in libraryList[artist][item]:
			songList.append([thesong[1],thesong[2]])

artistList = sorted(artistList, key = lambda x: x[0].lower())
artistListLength = len(artistList)
albumList = sorted(albumList, key = lambda x: x[0].lower())
albumListLength = len(albumList)
songList = sorted(songList, key = lambda x: x[0].lower())
songListLength = len(songList)

queue = random.sample(range(1,songListLength), round(songListLength/10))
queueCount = 0
#---------------------------------------------------------------------------------------------

#play the song -------------------------------------------------------------------------------
def songUpdate():
	global song
	global albumArt
	global tag
	tag = TinyTag.get(song, image=True)
	image_data = tag.get_image()
	with open(os.path.join('Assets', 'album.jpg'), "wb") as f:
	    f.write(image_data)
	albumArt = pygame.image.load(os.path.join('Assets', 'album.jpg'))
	albumArt = pygame.transform.scale(albumArt, (240,240))
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
#---------------------------------------------------------------------------------------------

def drawPlayDisplay(playBarJuice, song, album, artist, playTime, remainingTime):
	playBarEmpty_image = pygame.image.load(os.path.join('Assets', 'playBarEmpty.png'))
	playBarJuice_image = pygame.image.load(os.path.join('Assets', 'playBarJuice.png'))

	#rightsidetext WIN.blit(textvar, (240 - textvar.get_width() - 5, y))
	WIN.fill(ZumeGrey)
	WIN.blit(albumArt, (0,0))
	WIN.blit(playBarEmpty_image,(0,240))
	WIN.blit(playBarJuice_image, (playBarJuice.x,playBarJuice.y))

	remainingTimeText = boldSmall.render("-" + remainingTime, 1, ZumeLGrey)
	WIN.blit(remainingTimeText, (240 - remainingTimeText.get_width() -4 , 243))

	playTimeText = boldSmall.render(playTime, 1, ZumeLGrey)
	WIN.blit(playTimeText, (4, 243))

	songText = boldSmall.render(song, 1, ZumeWhite)
	WIN.blit(songText, (4, 267))
	
	albumText = boldSmall.render(album, 1, ZumeLGrey)
	WIN.blit(albumText, (4, 283))
	
	artistText = boldSmall.render(artist, 1, ZumeLGrey)
	WIN.blit(artistText, (4, 299))
	
	pygame.display.update()

def playDisplay():
	global song
	global queueCount
	playBarJuice = pygame.Rect(-240,240,240,3)
	#will need to move into an event at some point
	songUpdate()
	clock = pygame.time.Clock()
	
	run = True
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.DROPFILE:
				file_extension = os.path.splitext(event.file)[1]
				if file_extension in [".mp3", ".ogg", ".wav", ".flac"]:
					try:
						pygame.mixer.music.load(event.file) # load the music in the file name.
						song = event.file
						songUpdate()
						pygame.mixer.music.play()
					except:
						pass
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					pass
				elif event.key == pygame.K_UP or event.key == pygame.K_w:
					pass
				elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
					queueCount += -1
					song = songList[queue[queueCount]][1]
					songUpdate()
				elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					song = songList[queue[queueCount]][1]
					songUpdate()
					queueCount += 1
				elif event.key == pygame.K_RETURN:
					pass
				elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
					return
			if event.type == pygame.MOUSEBUTTONDOWN:				
				if event.button == 4: pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.01)
				if event.button == 5: pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.01)
			if event.type == MUSIC_END:
				song = songList[queue[queueCount]][1]
				songUpdate()
				queueCount += 1

		keys_pressed = pygame.key.get_pressed()
		if keys_pressed[pygame.K_SPACE]:
			if pygame.mixer.music.get_busy():
				pygame.mixer.music.pause()
			else:
				pygame.mixer.music.unpause()
		
		playTime = pygame.mixer.music.get_pos()
		
		songLength = (tag.duration)*1000 

		playBarJuice.x = ((playTime/songLength)*240)-240

		remainingTime = (tag.duration) - (playTime/1000)

		remainingTime = time.strftime('%M:%S', time.gmtime(remainingTime))
		playTime =  time.strftime('%M:%S', time.gmtime(playTime/1000))

		song = tag.title #bold
		album = tag.album
		artist = tag.artist
		

		drawPlayDisplay(playBarJuice, song, album, artist, playTime, remainingTime)

def drawDoItAllMenu(list):
	print(album)
	#maybe make the albums pull their songs in the  initial variable


#
#
#
#Needs to go into a sub or else I'll be making the list too many times
def doItAllMenu(varList):
	global musicMenuTop    #keeps track of the sub menu
	global subMenuCount
	varListLen = len(varList)

	WIN.fill((48, 46, 48)) #fill colour
	surfaceY = 25          #makes it all scrollable

	if subMenuCount >= 12 and subMenuCount < varListLen:
		surfaceY = ((subMenuCount - 13) * -18)
	elif subMenuCount == varListLen:
		subMenuCount = 0


	for x in range(subMenuCount - 15, subMenuCount):
		if x == subMenuCount and x > -1:
			sndMenuTop0 = smallFont.render(varList[x][0], 1, ZumeWhite)
			WIN.blit(sndMenuTop0, (38, ((x + 1) * 18) + surfaceY))
		elif x > -1:
			sndMenuTop0 = smallFont.render(varList[x][0], 1, ZumeLGrey)
			WIN.blit(sndMenuTop0, (38, ((x + 1) * 18) + surfaceY))

	for x in range(subMenuCount, subMenuCount+15):
		if x == subMenuCount:
			sndMenuTop0 = smallFont.render(varList[x][0], 1, ZumeWhite)
			WIN.blit(sndMenuTop0, (38, ((x + 1) * 18) + surfaceY))
		elif x < varListLen:
			sndMenuTop0 = smallFont.render(varList[x][0], 1, ZumeLGrey)
			WIN.blit(sndMenuTop0, (38, ((x + 1) * 18) + surfaceY))

	pygame.draw.rect(WIN, ZumeGrey, pygame.Rect(0, 0, 240, 42))
	sndMenuTop0 = medFont.render(musicMenuTop, 1, ZumeWhite)
	WIN.blit(sndMenuTop0, (40, -5))

	pygame.display.update()

def musicMenu(menuSelected):
	global musicMenuTop
	global subMenuCount
	topMenu = ['songs', 'artists', 'albums']

	def selectionMusicMenu(): #this is like if on artist
		global song
		if musicMenuTop == 'songs':
			song = songList[subMenuCount][1]
			songUpdate()
			playDisplay()
		elif musicMenuTop == 'artists':
			print(libraryList[str(artistList[subMenuCount][0])].keys())
			doItAllMenu(list(libraryList[str(artistList[subMenuCount][0])].keys()))
		elif musicMenuTop == 'albums':
			#doItAllMenu(libraryList[str(artistList[subMenuCount][0])])
			pass

	run = True
	while run:
		clock.tick(FPS)

		if musicMenuTop == 'songs':
			doItAllMenu(songList)
		elif musicMenuTop == 'albums':
			doItAllMenu(albumList)
		elif musicMenuTop == 'artists':
			doItAllMenu(artistList)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					subMenuCount += 1
				elif event.key == pygame.K_UP or event.key == pygame.K_w:
					subMenuCount += -1
				elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
					musicMenuTop = topMenu[(topMenu.index(musicMenuTop) - 1) % len(topMenu)]
				elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					musicMenuTop = topMenu[(topMenu.index(musicMenuTop) + 1) % len(topMenu)]
				elif event.key == pygame.K_RETURN:
					selectionMusicMenu()
				elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
					#pygame.quit()
					return		
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1: 
					selectionMusicMenu()		
				if event.button == 4: subMenuCount += -12 #ZOOOM CAN GO OVER LIST LENGTH
				if event.button == 5: subMenuCount += +12

def drawSettingsMenu():
	#fill the background
	WIN.fill(ZumeGrey)

	menuLabel = smallFont.render('drag your library here', 1, ZumeWhite)
	WIN.blit(menuLabel, (4,40))

	pygame.display.update()

def settingsMenu():
	clock = pygame.time.Clock()
	
	run = True
	while run:
		clock.tick(FPS)
		drawSettingsMenu()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.DROPFILE:
				# file_extension = os.path(event.file)[0]
				library(os.path.splitext(event.file)[0])
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					pass
				elif event.key == pygame.K_UP or event.key == pygame.K_w:
					pass
				elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
					pass
				elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					pass
				elif event.key == pygame.K_RETURN:
					pass
				elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
					return
			if event.type == pygame.MOUSEBUTTONDOWN:				
				pass
			if event.type == MUSIC_END:
				song = songList[queue[queueCount]][1]
				songUpdate()
				queueCount += 1

def drawMainMenu(mainList):
	global mainMenuCount

	#fill the background
	WIN.fill(ZumeGrey)

	#set y  position for the menu scroll
	surfaceY = 0

	# >=5 allows is for that weird almost full scroll 
	#then if at the end of the list go to top, then top up = go to bottom
	if mainMenuCount >= 5 and mainMenuCount < len(mainList):
		surfaceY = ((mainMenuCount - 4) * -40)
	elif mainMenuCount == len(mainList):
		mainMenuCount = 0
	elif mainMenuCount < 0:
		mainMenuCount = len(mainList) - 1 

	#draw the list with the  white highlight on the selection
	for i in range(len(mainList)):
		if i == mainMenuCount:
			menuLabel = lrgFont.render(mainList[i], 1, ZumeWhite)
			WIN.blit(menuLabel, (4, ((i + 1) * 40) + surfaceY))
		else:
			menuLabel = lrgFont.render(mainList[i], 1, ZumeLGrey)
			WIN.blit(menuLabel, (4, ((i + 1) * 40) + surfaceY))

	pygame.display.update()

def main():
	#set a global mainMenuCount so that we can draw it correctly and retain it during navigation
	global mainMenuCount
	#set as a list to facilitae the selection function
	mainList = ['music', 'videos', 'pictures', 'social', 'radio', 'marketplace', 'games', 'settings']

	#this function allows us to open the correct menu
	def selection():
		if mainList[mainMenuCount] == 'music': 
			musicMenu(mainList[mainMenuCount])
		elif mainList[mainMenuCount] == 'settings':
			#print('das')
			settingsMenu()
		else:
			pass

	#main loop every menu is essentially its own game, draw menu > check for events > then draw the results or call the next menu 
	run = True
	while run:
		#runs at global set fps 30 for preformance
		clock.tick(FPS)

		#draw the menu, send the list of items.
		drawMainMenu(mainList)

		#check for user events
		for event in pygame.event.get():
			if event.type == pygame.QUIT: #window close ends the program
				run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN or event.key == pygame.K_s: #down/s
					mainMenuCount += 1
				elif event.key == pygame.K_UP or event.key == pygame.K_w: #up/w
					mainMenuCount += -1
				elif event.key == pygame.K_RETURN: #enter is middle button on zume
					selection()
				elif event.key == pygame.K_SPACE: #space is play button on zume
					playDisplay()
				elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE: #backspace or escape is back/close
					run = False
			
			if event.type == pygame.MOUSEBUTTONDOWN: #mouse movements (click, scroll up, scroll down)
				if event.button == 1: selection()			
				if event.button == 4: mainMenuCount += -1
				if event.button == 5: mainMenuCount += +1

	pygame.quit()
	sys.exit()

def library(path):
	bigList = {}

	for root, dirs, files in os.walk(path):
		for file in files:
			#append the file name to the list
			ext = os.path.splitext(file)[1]

			if ext == ".mp3" or ext == ".wav" or ext == ".flac" or ext == ".ogg" or ext == ".mp3" or ext == ".mp3": #wma not supported by pygame mixer
				tag = TinyTag.get(os.path.join(root,file), image=True)
				print('dasd')
				print(tag.albumartist)
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
				bigList[artist][album] = sorted(bigList[artist][album], key=itemgetter(0))

	for album in bigList[artist][album]:
		album.sort()
	# print(bigList)
	
	with open('mylib.json', 'w') as f:
		json.dump(bigList, f)
		# save this as json and then bring it back.


if __name__ == "__main__":
	main()
