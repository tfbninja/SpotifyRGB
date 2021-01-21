from colour import Color
from SpotifyLiaison import getLoopLength
import pattern

def isDisco():
	return False

def utilizesRandom():
	return False

def getName():
	return "experiment_no_2"

class experiment_no_2(pattern):

	def __init__(self, now_playing):
		self.current_song = now_playing
		self.color_bounds = [Color('#4287f5'), Color('#d935db')]
		self.color = self.color_bounds[0]
		self.pulse_baseline = 0.3

	def iterate(self):

		# time between next beat and beat after that
		beat_time = self.current_song.getSecondsToNthBeat(2) - self.current_song.getSecondsToNthBeat(1)

		#the time it takes the SpotifyLiaison main loop to execute, not averaged or anything (i should probably fix
		# that, huh
		loop_length = getLoopLength()

		if self.color.hue > self.color_bounds[1].hue:
			ratio = 1 - (loop_length / (beat_time * 1000))
		elif self.color.hue < self.color_bounds[0].hue:
			ratio = (loop_length / (beat_time * 1000))

		self.color.hue = (ratio * (self.color_bounds[0].hue - self.color_bounds[1].hue)) + self.color_bounds[0].hue

	def getColor(self):
		return self.color

	def processSongChange(self):
		self.color = self.color_bounds[0]
