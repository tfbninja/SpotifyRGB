from colour import Color
from SpotifyLiaison import getLoopLength
import pattern

def isDisco():
	return False

def utilizesRandom():
	return False

def getName():
	return "beat_swirl"

class beat_swirl(pattern):

	def __init__(self, now_playing):
		self.current_song = now_playing
		self.starting_color = Color('#38e84c')
		self.color = self.starting_color
		self.pulse_baseline = 0.3

	def iterate(self):
		# Calculates time of one and a half beats in millis
		one_and_a_half_beat_time = ((self.current_song.getSecondsToNthBeat(4) -
		                             self.current_song.getSecondsToNthBeat(1)) / 2) * 1000

		# calculates ratio of one loop time to one and a half
		# beat time, all in millis
		ratio = getLoopLength() / one_and_a_half_beat_time

		self.color.hue += (ratio * 0.5) % 1

	def getColor(self):
		return self.color

	def processSongChange(self):
		self.color = self.starting_color
