# This Python file uses the following encoding: utf-8
from tinytag import TinyTag
import pygame
import os, io, time, libraryListFile, random, sys

#initialise pygame and font ------------------------------------------------------------------
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.01)
pygame.key.set_repeat(250)
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
#menuCount = 0
FPS = 30
#---------------------------------------------------------------------------------------------

#working with variables---------------------------------------------------------------------
libraryList = libraryListFile.libraryListFile
artistList = []
albumList = []
songList = []
for artist in libraryList:
	artistList.append(str(artist))
	for item in list(libraryList[artist].keys()):
		albumList.append(item)
		for thing in libraryList[artist][item]:
			songList.append([thing[1],thing[2]])

artistList = sorted(artistList, key=str.casefold)
artistListLength = len(artistList)
albumList = sorted(albumList, key=str.casefold)
albumListLength = len(albumList)
songList = sorted(songList, key = lambda x: x[0].lower())
songListLength = len(songList)

queue = random.sample(range(1,songListLength), 10)
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

def drawSecondMenu(menuCount):
	# global menuCount
	WIN.fill((48, 46, 48))
	surfaceY = 25
	if menuCount >= 12 and menuCount < songListLength:
		surfaceY = ((menuCount - 13) * -18)
	elif menuCount == songListLength:
		menuCount = 0

#songs-----------------------------------------------------------------------------------------
	# sndMenuTop0 = medFont.render("songs", 1, ZumeWhite)
	# WIN.blit(sndMenuTop0, (40, -5))

	# for x in range(menuCount - 15, menuCount):
	# 	if x == menuCount:
	# 		sndMenuTop0 = smallFont.render(songList[x][0], 1, ZumeWhite)
	# 		WIN.blit(sndMenuTop0, (38, ((x + 1) * 18) + surfaceY))
	# 	else:
	# 		sndMenuTop0 = smallFont.render(songList[x][0], 1, ZumeLGrey)
	# 		WIN.blit(sndMenuTop0, (38, ((x + 1) * 18) + surfaceY))

	# for x in range(menuCount, menuCount+15):

	# 	if x == menuCount:
	# 		sndMenuTop0 = smallFont.render(songList[x][0], 1, ZumeWhite)
	# 		WIN.blit(sndMenuTop0, (38, ((x + 1) * 18) + surfaceY))
	# 	else:
	# 		sndMenuTop0 = smallFont.render(songList[x][0], 1, ZumeLGrey)
	# 		WIN.blit(sndMenuTop0, (38, ((x + 1) * 18) + surfaceY))
#---------------------------------------------------------------------------------------------

#albums---------------------------------------------------------------------------------------
	# sndMenuTop0 = medFont.render("albums", 1, ZumeWhite)
	# WIN.blit(sndMenuTop0, (40, -5))

	# for x in range(menuCount - 15, menuCount):
	# 	if x == menuCount:
	# 		sndMenuTop0 = smallFont.render(albumList[x], 1, ZumeWhite)
	# 		WIN.blit(sndMenuTop0, (38, ((x + 1) * 18) + surfaceY))
	# 	else:
	# 		sndMenuTop0 = smallFont.render(albumList[x], 1, ZumeLGrey)
	# 		WIN.blit(sndMenuTop0, (38, ((x + 1) * 18) + surfaceY))

	# for x in range(menuCount, menuCount+15):

	# 	if x == menuCount:
	# 		sndMenuTop0 = smallFont.render(albumList[x], 1, ZumeWhite)
	# 		WIN.blit(sndMenuTop0, (38, ((x + 1) * 18) + surfaceY))
	# 	else:
	# 		sndMenuTop0 = smallFont.render(albumList[x], 1, ZumeLGrey)
	# 		WIN.blit(sndMenuTop0, (38, ((x + 1) * 18) + surfaceY))
#---------------------------------------------------------------------------------------------

#artists--------------------------------------------------------------------------------------
	sndMenuTop0 = medFont.render("artists", 1, ZumeWhite)
	WIN.blit(sndMenuTop0, (40, -5))

	for x in range(menuCount - 15, menuCount):
		if x == menuCount:
			sndMenuTop0 = smallFont.render(artistList[x], 1, ZumeWhite)
			WIN.blit(sndMenuTop0, (38, ((x + 1) * 18) + surfaceY))
		else:
			sndMenuTop0 = smallFont.render(artistList[x], 1, ZumeLGrey)
			WIN.blit(sndMenuTop0, (38, ((x + 1) * 18) + surfaceY))

	for x in range(menuCount, menuCount+15):

		if x == menuCount:
			sndMenuTop0 = smallFont.render(artistList[x], 1, ZumeWhite)
			WIN.blit(sndMenuTop0, (38, ((x + 1) * 18) + surfaceY))
		else:
			sndMenuTop0 = smallFont.render(artistList[x], 1, ZumeLGrey)
			WIN.blit(sndMenuTop0, (38, ((x + 1) * 18) + surfaceY))
#---------------------------------------------------------------------------------------------
	pygame.display.update()

def secondMenu(menuCount):
	global song
	run = True
	while run:
		clock.tick(FPS)

		drawSecondMenu(menuCount)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					menuCount += 1
				elif event.key == pygame.K_UP or event.key == pygame.K_w:
					menuCount += -1
				elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
					pass
				elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					pass
				elif event.key == pygame.K_RETURN:
					song = songList[menuCount][1]
					songUpdate()
					menuCount = 0
					playDisplay()
				elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
					#pygame.quit()
					return		
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1: 
					song = songList[menuCount][1]
					songUpdate()	
					menuCount = 0
					playDisplay()			
				if event.button == 4: menuCount += -1
				if event.button == 5: menuCount += +1

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
					pass
				elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					pass
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
		
		songLength = (tag.duration*2)*1000  #TINY TAG THINKS SONG IS HALF LENGTH? Possible that it's the bitrate?

		playBarJuice.x = ((playTime/songLength)*240)-240

		remainingTime = (tag.duration*2) - (playTime/1000)

		remainingTime = time.strftime('%M:%S', time.gmtime(remainingTime))#TINY TAG THINKS SONG IS HALF LENGTH? Possible that it's the bitrate?
		playTime =  time.strftime('%M:%S', time.gmtime(playTime/1000))

		song = tag.title #bold
		album = tag.album
		artist = tag.artist
		

		drawPlayDisplay(playBarJuice, song, album, artist, playTime, remainingTime)
		
	pygame.quit()

def drawMainMenu(surface, menuCount):
	WIN.fill(ZumeGrey)

	mainList = ['music', 'videos', 'pictures', 'social', 'radio', 'marketplace', 'games', 'settings']

	surfaceY = 0
	i = 0

	if menuCount >= 5 and menuCount < len(mainList):
		surfaceY = ((menuCount - 4) * -40)
	elif menuCount == len(mainList):
		menuCount = 0

	for x in mainList:
		if i == menuCount:
			mMenu0 = lrgFont.render(x, 1, ZumeWhite)
			WIN.blit(mMenu0, (4, ((i + 1) * 40) + surfaceY))
		else:
			mMenu0 = lrgFont.render(x, 1, ZumeLGrey)
			WIN.blit(mMenu0, (4, ((i + 1) * 40) + surfaceY))

		i += 1


	pygame.display.update()

def main():
	menuCount = 0
	global surfacePos 
	surfacePos = 0
	run = True
	while run:
		clock.tick(FPS)

		surface = pygame.Rect(0,0,240,1000)
		drawMainMenu(surface, menuCount)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					menuCount += 1
				elif event.key == pygame.K_UP or event.key == pygame.K_w:
					menuCount += -1
				elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
					pass
				elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					pass
				elif event.key == pygame.K_RETURN:
					secondMenu(0)
				elif event.key == pygame.K_SPACE:
					playDisplay()
				elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
					run = False
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1: secondMenu(0)				
				if event.button == 4: menuCount += -1
				if event.button == 5: menuCount += +1


			keys_pressed = pygame.key.get_pressed()
			if keys_pressed[pygame.K_x]:
				print ('xdown') #keeps going while held
		
	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()
