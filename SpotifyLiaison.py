from patterns2 import *
import colorsys  # see colour import for why i need to import TWO color libraries
import random
import time
from math import *

import serial.tools.list_ports
import spotipy
from colour import Color  # WHY NO HSV SUPPORT C'MON (literal rage but at the same time i get it)
from spotipy.oauth2 import SpotifyOAuth

import NowPlaying
from credentials import *

"""
def refreshRandoms():  # re-does all the random components
	fastRandomDiscoColors = [randomishColor(), randomishColor(), randomishColor(), randomishColor()]
	# print("fast random disco colors: " + str(fastRandomDiscoColors))

	randMultiplier = float(random.randint(10, 100)) / 100
	randExponentiator = float(random.randint(10, 100)) / 100

	# print("randmult: " + str(randMultiplier) + " randExp: " + str(randExponentiator))
"""

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

"""
def resetVariablesBecauseSongChanged():
	discoesDone = 0
	lastDiscoBeat = 0
	time_signature_last_tatum_no = 0
	lastOscillationBeat = 0
"""

"""
def nextPattern(currentSong, currentPattern):
	successful = False
	while not successful:
		try:
			canBeDisco = discoesDone < discoesPerSong and not getSection(
				currentSong) == 0  # You don't want the lights doing too many disco patterns, so we make sure we
		# haven't done more than the allowed amount, also you don't want a disco at the beginning of the song
		# most likely

		except IndexError as I:
			currentSong.reSync()
			print(type(I), I)
		except TypeError as T:
			currentSong.reSync()
			print(type(T), T)

	if canBeDisco:
		validChoices = [*range(len(patterns))]
		validChoices.remove(currentPattern)
	else:
		validChoices = []
		for i in nonDiscoPatterns:
			validChoices.append(i[1])
	newPattern = random.choice(validChoices)
	print("new pattern is " + str(patterns[newPattern]))
	print("next section is in " + str(getTimeToNextSection(currentSong))[:5] + "s")
	return newPattern
"""

def getValue(color):
	val = colorsys.rgb_to_hsv(color.red, color.green, color.blue)[2]
	return val

def setValue(color, val):
	oldColor = colorsys.rgb_to_hsv(color.red, color.green, color.blue)
	output = Color(rgb=colorsys.hsv_to_rgb(oldColor[0], oldColor[1], val))
	return output

def flushSerialBuffers():
	ser.flushInput()
	ser.flushOutput()

def getDiscoBar():
	return discoBar

def getLoopLength():
	return loopLength

def printStatusToUser(currentSong, pattern_manager):
	print("Now playing: " + currentSong.getName())
	print("The current pattern is " + str(pattern_manager.getPatternName()))
	print("next section is in " + str(currentSong.getSecondsToNextSection())[:5] + "s")

	time_signature = currentSong.getTimeSignature()
	print("Time signature: " + str(time_signature))

# fair warning, I know that I'm using the term 'disco' wrong, it should be strobe, but by the time I wanted to change
# it, it was too late
#patterns = ['color_swirl', 'red_white_blue_disco', 'beat_swirl', 'experiment_no_2', 'rand_color_swirl',
#            'disco_but_with_different_colors', 'super_fast_disco_and_also_random_colors_because_i_said',
#            'gentle_pulse', 'time_signature_pulse', '2_color_oscillation']

"""
nonDiscoPatterns = []  # this list will be a list of lists, where each sublist is a pattern, and it's corresponding
# indice in patterns[]
for i in range(len(patterns)):
	if not ("disco" in patterns[i]):
		nonDiscoPatterns.append([patterns[i], i])
"""

syncPeriod = 250
loopIndiceResetPeriod = 2000
discoesPerSong = 2
discoesDone = 0
currentPattern = 0


"""
startingColor = Color("Red")
# print(getValue(startingColor))
# print(setValue(startingColor, 0.5))
startingHueIncrement = 0.001

pulseBaseline = 0.3  # how dark in value (HSV) a pulsing pattern should ever get

discoBar = 0.050  # in seconds (50 millis)
currentHue = 0
lastDiscoBeat = 0

disco_but_with_different_colors_hue_change_time_ms = 50  # naming things is hard, ok?

exp_no_2_color = Color('#4287f5')
exp_no_2_color_bounds = [Color('#4287f5'), Color('#d935db')]
exp_no_2_ratio = 0.5

currentPolarColor = Color('#38e84c')

time_signature_pulse_color = Color("#44f25b")
time_signature_pulse_hue_add = 0.31
time_signature_indice = 0
time_signature_last_tatum_no = 0
time_signature = 4

oscillation_colors = [Color('#34ebcf'), Color('#d66f1c')]
lastOscillationBeat = 0
oscillation_first_color = False
color_ratio = 0
"""

loopLength = 0.001

# Spotify variable, manages all API requests
sp = spotipy.Spotify(
	auth_manager=SpotifyOAuth(client_id=id, client_secret=secret, redirect_uri="https://example.com/callback",
	                          scope="user-read-currently-playing"))
# The currentSong object stores all the cached data about the song, including the beatlist, time signature,
# danceability, and so forth
currentSong = NowPlaying.NowPlaying(sp)
# add patterns from patterns folder somehow idk
pattern_list = [] # FIXME
pattern_manager = patternManager(currentSong, pattern_list, currentPattern, discoesPerSong, discoesDone) # FIXME too
printStatusToUser(currentSong)

"""
# This re-calculates the random variables for the patterns that utilize randomness
refreshRandoms()
"""


# This is an integer describing the section in the song that we last knew we were in, if the CURRENT section changes,
# we know to change the pattern
lastSection = getSection(currentSong)

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

# c is the variable we're using to store the color we're going to send over Serial to the Arduino
c = startingColor

# This is the indice for the loop that we are in, when it gets above loopIndiceResetPeriod, it resets to 0
loopIndice = 0

# This is the main loop, where all the pattern algorithms are run
while True:

	# We time the loop length, necessary for at least one pattern
	loopStart = time.time()

	if currentSong.isPlaying():
		try:
			# This checks if we're near the end of the song
			if currentSong.getPosInSongMillis() >= currentSong.getSongLengthMillis() - 3005:  # 3000 for my crossfade level, -5 for caution
				currentSong.reSync()
				resetVariablesBecauseSongChanged()  # fairly self-explanatory, no? Thank you, I take great pride in that function name.

			# This checks if we are in the first 5000 milliseconds of the song, because we've still got to query Spotify for all the info, so we'll just do a simple color change for the time being
			if currentSong.getPosInSongMillis() < 5000:
				# change the hue slightly
				c.hue += startingHueIncrement
			else:
				try:
					# if we JUST changed sections, we want to update a few things
					if getSection(currentSong) != lastSection:
						print("next section is in " + str(getTimeToNextSection(currentSong))[:5] + "s")
						lastSection = getSection(currentSong)
						refreshRandoms()
						currentPattern = nextPattern(currentSong, currentPattern)
				except IndexError as I:
					c.hue += startingHueIncrement
					currentSong.reSync()
					print(type(I), I)
				except TypeError as T:
					c.hue += startingHueIncrement
					currentSong.reSync()
					print(type(T), T)

				if patterns[currentPattern] == 'color_swirl':
					if c.hue < 0.998:
						c.hue = c.hue + 0.0005
					else:
						c.hue = 0

					# please excuse my lack of knowledge of how to not repeat these numerous stupid try/except statments
					try:
						nextBeat = getTimeToNextBeat(currentSong)
					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					try:
						lastBeat = getTimeSinceBeat(currentSong)
					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					try:
						# this ratio is the ratio of how far along in the beat we are, if its right before the next beat
						# it should be near 1. if we just had a beat, it should be near 0
						ratio = (nextBeat) / ((nextBeat + lastBeat) / 2) * (1 - pulseBaseline) + pulseBaseline
					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					# to get a pulsing effect, we apply the ratio calculated earlier to the value level of the color we've already assigned
					c = setValue(c, max(min(ratio, 1), 0))
				elif patterns[currentPattern] == 'disco':
					hues = [Color("Red"), Color("Blue"), Color("White")]

					if getBeat(currentSong) > lastDiscoBeat + 1:  # change hues every other beat
						lastDiscoBeat = getBeat(currentSong)
						currentHue += 1
						if currentHue > len(hues) - 1:
							currentHue = 0
					c = hues[currentHue]

					try:
						nextTatum = getTimeToNextTatum(currentSong)
					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					try:
						lastTatum = getTimeSinceTatum(currentSong)

					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					if nextTatum <= discoBar / 2 or lastTatum <= discoBar / 2:
						c.red *= 1
						c.green *= 1
						c.blue *= 1
					else:
						c.red *= 0.01
						c.green *= 0.01
						c.blue *= 0.01
				elif patterns[
					currentPattern] == 'beat_swirl':  # don't ask me what this pattern calculates, all i know is that the color change seeems to be in time with the beat \_:)_/
					oneAndAHalfBeatTime = (getTimeToNthBeat(currentSong, 4) - getTimeToNthBeat(currentSong,
					                                                                           1)) / 2 * 1000  # Calculates time of one and a half beats in millis
					ratio = (
						        loopLength) / oneAndAHalfBeatTime  # calculates ratio of one loop time to one and a half beat time, all in millis
					currentPolarColor.hue += (ratio * 0.5) % 1
					c = currentPolarColor
				elif patterns[currentPattern] == 'experiment_no_2':

					try:
						beatTime = getTimeToNthBeat(currentSong, 2) - getTimeToNthBeat(currentSong,
						                                                               1)  # time between next beat and beat after that

					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					if exp_no_2_color.hue > exp_no_2_color_bounds[1].hue:
						exp_no_2_ratio = 1 - (loopLength / (beatTime * 1000))
					elif exp_no_2_color.hue < exp_no_2_color_bounds[0].hue:
						exp_no_2_ratio = (loopLength / (beatTime * 1000))

					exp_no_2_color.hue = (exp_no_2_ratio * (
							exp_no_2_color_bounds[0].hue - exp_no_2_color_bounds[1].hue)) + exp_no_2_color_bounds[
						                     0].hue
					c = exp_no_2_color
				elif patterns[currentPattern] == 'rand_color_swirl':  # random color swirl, sometimes speeds up, sometimes slows down
					if c.hue < 0.998:
						c.hue = c.hue + random.randint(-1, 5) / 10000
					else:
						c.hue = 0

					try:
						nextBeat = getTimeToNextBeat(currentSong)

					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					try:
						lastBeat = getTimeSinceBeat(currentSong)

					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					try:
						ratio = (nextBeat ** 2) / (nextBeat + lastBeat ** 2)

					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					c = setValue(c, min(ratio + 0.05, 1))
				elif patterns[
					currentPattern] == 'disco_but_with_different_colors':  # its like the disco function but not just red/white/blue
					discoColorHues = [Color('#4ec7c1'), Color('#8715a3'), Color('#d6a727'), Color('#8a0615')]

					if getBeat(currentSong) > lastDiscoBeat + 1:  # change hues every other beat
						lastDiscoBeat = getBeat(currentSong)
						currentHue += 1
						if currentHue > len(discoColorHues) - 1:
							currentHue = 0
					c = discoColorHues[currentHue]

					try:
						nextTatum = getTimeToNextTatum(currentSong)

					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					try:
						lastTatum = getTimeSinceTatum(currentSong)

					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					# basically we turn the lights on at full blast for discoBar length in seconds centered at the tatum's time
					if nextTatum <= discoBar / 2 or lastTatum <= discoBar / 2:
						c.red *= 1
						c.green *= 1
						c.blue *= 1
					else:
						c.red *= 0.01
						c.green *= 0.01
						c.blue *= 0.01
				elif patterns[
					currentPattern] == 'super_fast_disco_and_also_random_colors_because_i_said':  # its like the disco function but not just red white or blue
					hues = [Color('#4ec7c1'), Color('#8715a3'), Color('#d6a727'), Color('#8a0615')]

					if getBeat(currentSong) > lastDiscoBeat + 1:  # change hues every other beat
						lastDiscoBeat = getBeat(currentSong)
						currentHue += 1
						if currentHue > len(hues) - 1:
							currentHue = 0
					c = hues[currentHue]

					try:
						nextTatum = getTimeToNextTatum(currentSong)

					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					try:
						lastTatum = getTimeSinceTatum(currentSong)

					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					if nextTatum <= discoBar / 2 or lastTatum <= discoBar / 2:
						c.red *= 1
						c.green *= 1
						c.blue *= 1
					else:
						c.red *= 0.01
						c.green *= 0.01
						c.blue *= 0.01
				elif patterns[currentPattern] == 'gentle_pulse':
					if c.hue < 0.998:
						c.hue = c.hue + 0.0005
					else:
						c.hue = 0

					try:
						nextBeat = getTimeToNextBeat(currentSong)

					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					try:
						lastBeat = getTimeSinceBeat(currentSong)

					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					try:
						ratio = (0.2 * ((nextBeat) / (nextBeat + lastBeat))) ** 0.8

					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					c = setValue(c, ratio)
				elif patterns[currentPattern] == 'time_signature_pulse':
					if time_signature_indice == time_signature:
						time_signature_indice = 0
						time_signature_pulse_color.hue += time_signature_pulse_hue_add
						time_signature_pulse_color.hue = time_signature_pulse_color.hue % 1
					c = Color(time_signature_pulse_color)

					try:
						nextTatum = getTimeToNextTatum(currentSong)

					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					try:
						lastTatum = getTimeSinceTatum(currentSong)

					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					try:
						ratio = (nextTatum ** 2) / (nextTatum + lastTatum ** 2)
					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					if getTatum(currentSong) > time_signature_last_tatum_no:
						time_signature_last_tatum_no = getTatum(currentSong)
						time_signature_indice += 1

					c = setValue(c, ratio + 0.05)
				elif patterns[currentPattern] == '2_color_oscillation':

					try:
						thisBeat = getBeat(currentSong)

					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						currentSong.reSync()
						c.hue += startingHueIncrement
						print(type(T), T)

					if thisBeat > lastOscillationBeat:
						lastOscillationBeat = thisBeat
						oscillation_first_color = not oscillation_first_color

					try:
						nextBeat = getTimeToNextBeat(currentSong)

					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)

					lastBeat = getTimeSinceBeat(currentSong)

					try:
						lum_ratio = min(max((nextBeat ** 2) / ((nextBeat + lastBeat) ** 2) / 2, 0), 1)
						color_ratio = lum_ratio  # nextBeat / ((lastBeat + nextBeat) / 2)
						if color_ratio > 0.5:
							color_ratio = 1 - ((1 - color_ratio) ** 2)
						else:
							color_ratio = color_ratio ** 2

					except IndexError as I:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(I), I)
					except TypeError as T:
						c.hue += startingHueIncrement
						currentSong.reSync()
						print(type(T), T)
					if oscillation_first_color:
						c.red = (color_ratio * oscillation_colors[0].red) + (
								(1 - color_ratio) * oscillation_colors[1].red)
						c.green = (color_ratio * oscillation_colors[0].green) + (
								(1 - color_ratio) * oscillation_colors[1].green)
						c.blue = (color_ratio * oscillation_colors[0].blue) + (
								(1 - color_ratio) * oscillation_colors[1].blue)
					else:
						c.red = ((1 - color_ratio) * oscillation_colors[0].red) + (
								color_ratio * oscillation_colors[1].red)
						c.green = ((1 - color_ratio) * oscillation_colors[0].green) + (
								color_ratio * oscillation_colors[1].green)
						c.blue = ((1 - color_ratio) * oscillation_colors[0].blue) + (
								color_ratio * oscillation_colors[1].blue)

					c = setValue(c, max(0, min(lum_ratio + 0.05, 1)))
				else:
					print("unknown pattern \"" + str(
						currentPattern) + "\"")  # haven't had this happen yet but i figured a big if like this should have an else

		except IndexError as I:
			c.hue += startingHueIncrement
			currentSong.reSync()
			print(type(I), I)
		except TypeError as T:
			c.hue += startingHueIncrement
			currentSong.reSync()
			print(type(T), T)
	else:
		c.hue += startingHueIncrement
		print(c)
	convertedRGB = [max(min(floor(c.red * 255), 255), 0), max(min(floor(c.green * 255), 255), 0),
	                max(min(floor(c.blue * 255), 255), 0)]

	out = '(' + str(convertedRGB[0]) + ',' + str(convertedRGB[1]) + ',' + str(convertedRGB[2]) + ')'

	# print(out)
	time.sleep(0.001)  # i had a really weird bug for a while where if i didn't have a print function executing every
	# single iteration, the lights didn't work. I figured out that my arduino serial was overwhelmed lol
	ser.write(bytes(out, 'utf-8'))  # tell the arduino what color to display! format: '(RED, GREEN, BLUE)', where RED,
	# GREEN, and BLUE are integers between 0 and 255

	if loopIndice % 150 == 0:
		# the serial would bug out after a while if i didn't do this regularly
		flushSerialBuffers()
	if loopIndice % syncPeriod == 0:
		# make sure we're still doing lights to the right song/beat
		currentSong.reSync()
	if loopIndice % loopIndiceResetPeriod == 0:
		loopIndice = 0

	loopIndice += 1
	loopLength = (time.time() - loopStart) * 1000
