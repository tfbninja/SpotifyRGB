import time
from math import floor

from colour import Color

from patterns2.pattern import pattern

class experiment_no_two(pattern):

	@staticmethod
	def isDisco():
		return False

	@staticmethod
	def getName():
		return "experiment_no_two"

	def __init__(self, now_playing):
		self.current_song = now_playing
		self.color_bounds = [Color('#4287f5'), Color('#d935db')]
		if self.color_bounds[1].hue < self.color_bounds[0].hue:
			self.color_bounds.reverse()
		self.color = self.color_bounds[0]
		self.color.hue -= 0.005
		self.loop_len_millis = 5
		self.ratio = 0.010

	def iterate(self):

		# time between next beat and beat after that
		beat_time_millis = floor((self.current_song.getSecondsToNthBeat(2) - self.current_song.getSecondsToNthBeat(1)) \
		                         * 1000)

		if self.color.hue > self.color_bounds[1].hue:
			self.ratio = -(float(self.loop_len_millis) / float(beat_time_millis))
		elif self.color.hue < self.color_bounds[0].hue:
			self.ratio = (float(self.loop_len_millis) / float(beat_time_millis))

		self.color.hue += (self.ratio * (self.color_bounds[1].hue - self.color_bounds[0].hue))

	def getColor(self):
		return self.color

	def processSongChange(self):
		if self.color_bounds[1].hue < self.color_bounds[0].hue:
			self.color_bounds.reverse()
		self.color = self.color_bounds[0]
		self.ratio = 0.001
