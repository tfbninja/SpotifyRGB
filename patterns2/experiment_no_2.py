from colour import Color

from patterns2.pattern import pattern


class experiment_no_2(pattern):

	@staticmethod
	def isDisco():
		return False

	@staticmethod
	def getName():
		return "experiment_no_2"

	def __init__(self, now_playing):
		self.current_song = now_playing
		self.color_bounds = [Color('#4287f5'), Color('#d935db')]
		self.color = self.color_bounds[0]
		self.pulse_baseline = 0.3
		self.manual_spotify_liaison_loop_len = 0.001

	def iterate(self):

		# time between next beat and beat after that
		beat_time = self.current_song.getSecondsToNthBeat(2) - self.current_song.getSecondsToNthBeat(1)


		if self.color.hue > self.color_bounds[1].hue:
			ratio = 1 - (self.manual_spotify_liaison_loop_len / (beat_time * 1000))
		elif self.color.hue < self.color_bounds[0].hue:
			ratio = (self.manual_spotify_liaison_loop_len / (beat_time * 1000))

		self.color.hue = (ratio * (self.color_bounds[0].hue - self.color_bounds[1].hue)) + self.color_bounds[0].hue

	def getColor(self):
		return self.color

	def processSongChange(self):
		self.color = self.color_bounds[0]
