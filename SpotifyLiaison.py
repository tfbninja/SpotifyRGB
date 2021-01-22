import random
import time
from math import *

import serial.tools.list_ports
import spotipy
from colour import Color  # WHY NO HSV SUPPORT C'MON (literal rage but at the same time i get it)
from spotipy.oauth2 import SpotifyOAuth

import NowPlaying
from credentials import *
from patterns2 import patternManager

def printDelta(start, message):
	print(str(time.time() - start) + "   " + message)

# in my highly uneducated opinion, this tends to generate colors that are highly saturated in the red, green,
# or blue direction. This is because one of the r,g,or b is likely to be high, and the others are likely to be lower
def randomishColor():
	total = random.randint(0, 255 * 3)
	random1 = random.randint(0, min(255, total))
	random2 = random.randint(0, min(255, total - random1))
	random3 = random.randint(0, min(255, total - (random1 + random2)))
	randoms = [float(random1), float(random2), float(random3)]
	random.shuffle(randoms)
	outColor = Color(rgb=(randoms[0] / 256, randoms[1] / 256, randoms[2] / 256))
	return outColor

def randomishColorSeed(seed):
	random_obj = random.random(seed)
	total = random_obj.randint(0, 255 * 3)
	random1 = random_obj.randint(0, min(255, total))
	random2 = random_obj.randint(0, min(255, total - random1))
	random3 = random_obj.randint(0, min(255, total - (random1 + random2)))
	randoms = [float(random1), float(random2), float(random3)]
	random_obj.shuffle(randoms)
	outColor = Color(rgb=(randoms[0] / 256, randoms[1] / 256, randoms[2] / 256))
	return outColor

def flushSerialBuffers():
	ser.flushInput()
	ser.flushOutput()

def getLoopLength():
	return loopLength

def printStatusToUser(current_song, pattern_manager):
	print("Now playing: " + current_song.getName())
	print("The current pattern is " + str(pattern_manager.getPatternName()))
	print("next section is in " + str(current_song.getSecondsToNextSection())[:5] + "s")

	time_signature = current_song.getTimeSignature()
	print("Time signature: " + str(time_signature))

def nextRandomPattern(currentSong, pattern_manager):
	pattern_manager.nextRandomPattern()
	printStatusToUser(currentSong, pattern_manager)

def nextPattern(pattern_manager, pattern_name):
	pattern_manager.nextPattern(pattern_name)
	printStatusToUser(current_song, pattern_manager)

def reSync(current_song, loop_indice, last_sync_indice, sync_period):
	if loop_indice - sync_period > last_sync_indice:
		current_song.reSync()
		return loop_indice
	return last_sync_indice

def hardReSync(current_song, loop_indice, last_hard_sync_indice, hard_sync_period):
	if loop_indice - hard_sync_period > last_hard_sync_indice:
		current_song.hardReSync()
		return loop_indice
	return last_hard_sync_indice

sync_period = 2000
hard_sync_period = sync_period
last_sync_indice = 0
last_hard_sync_indice = 0
strobes_per_song = 2
strobes_done = 0
current_pattern = 0

loopLength = 0.001

# Spotify variable, manages all API requests
sp = spotipy.Spotify(
	auth_manager=SpotifyOAuth(client_id=id, client_secret=secret, redirect_uri="https://example.com/callback",
	                          scope="user-read-currently-playing"))
# The currentSong object stores all the cached data about the song, including the beatlist, time signature,
# danceability, and so forth
current_song = NowPlaying.NowPlaying(sp)
# add patterns from patterns folder somehow idk
pattern_list = []  # FIXME (maybe)
pattern_manager = patternManager.patternManager(current_song, pattern_list, current_pattern, strobes_per_song,
                                                strobes_done)  #
printStatusToUser(current_song, pattern_manager)

# This is an integer describing the section in the song that we last knew we were in, if the CURRENT section changes,
# we know to change the pattern
lastSection = current_song.getSection()
lastURI = current_song.getURI()

# This gets a list of all (i think) devices
devices = [port.device for port in serial.tools.list_ports.comports()]
# this makes a list of the respective ports for each device, but only if they're the ones valid for me (you might
# have to change these if you use a different Arduino than I do)
ports = [port for port in devices if port in ['/dev/ttyACM0', '/dev/ttyUSB0', 'COM3']]
if len(ports) != 1:
	raise Exception('cannot identify port to use')
# Uses the first available serial device
port = ports[0]
ser = serial.Serial(port, 74880)
flushSerialBuffers()

# c is the variable we're using to store the color we're going to send over Serial to the Arduino
c = Color("Blue")

# This is the indice for the loop that we are in, when the song changes it resets to 0
loop_indice = 0

# This is the main loop, where all the pattern algorithms are run
while True:

	# We time the loop length, necessary for at least one pattern
	loopStart = time.time()

	if current_song.isPlaying():

		# This checks if we're near the end of the song
		# 3000 for my crossfade, 3000 for caution
		if current_song.getPosInSongMillis() >= current_song.getSongLengthMillis() - 6000:
			pattern_manager.processSongChange()
			nextPattern(pattern_manager, 'basic_hue_change')
			last_sync_indice = last_hard_sync_indice = hardReSync(current_song, loop_indice, last_hard_sync_indice,
			                                                      hard_sync_period)
			loop_indice = 0

		# This checks if we are in the first 5000 milliseconds of the song, because we've still got to query Spotify for all the info, so we'll just do a simple color change for the time being
		elif current_song.getPosInSongMillis() < 5000:
			pattern_manager.nextPattern('basic_hue_change')
			pass
		elif pattern_manager.getPatternName() == 'basic_hue_change':
			nextRandomPattern(current_song, pattern_manager)
		else:
			# if we JUST changed sections, we want to update a few things
			this_section = current_song.getSection()
			if this_section != lastSection:
				lastSection = this_section
				nextRandomPattern(current_song, pattern_manager)
				printStatusToUser(current_song, pattern_manager)

			pattern_manager.iteratePatternColor()
	else:
		nextPattern(pattern_manager, 'basic_hue_change')
		pass
	c = pattern_manager.getPatternColor()
	convertedRGB = [max(min(floor(c.red * 255), 255), 0), max(min(floor(c.green * 255), 255), 0),
	                max(min(floor(c.blue * 255), 255), 0)]

	out = '(' + str(convertedRGB[0]) + ',' + str(convertedRGB[1]) + ',' + str(convertedRGB[2]) + ')'

	# print(out)
	time.sleep(0.005)  # i had a really weird bug for a while where if i didn't have a print function executing every
	# single iteration, the lights didn't work. I figured out that my arduino serial was overwhelmed lol
	ser.write(bytes(out, 'utf-8'))  # tell the arduino what color to display! format: '(RED, GREEN, BLUE)', where RED,
	# GREEN, and BLUE are integers between 0 and 255

	if loop_indice % 50 == 0:
		# the serial would bug out after a while if i didn't do this regularly
		flushSerialBuffers()
	if loop_indice - last_sync_indice > sync_period:
		# make sure we're still doing lights to the right song/beat
		last_sync_indice = reSync(current_song, loop_indice, last_sync_indice, sync_period)

	loop_indice += 1
	loopLength = (time.time() - loopStart) * 1000
