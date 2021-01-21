from colour import Color

import pattern
from SpotifyLiaison import setValue

def isDisco():
	return False

def utilizesRandom():
	return False

def getName():
	return "two_color_oscillation"

class two_color_oscillation(pattern):

	def __init__(self, now_playing):
		self.current_song = now_playing
		self.oscillation_colors = [Color('#34ebcf'), Color('#d66f1c')]
		self.first_color = True
		if self.first_color:
			self.color = self.oscillation_colors[0]
		else:
			self.color = self.oscillation_colors[1]
		self.last_oscillation_beat = 0

	def iterate(self):

		this_beat = self.current_song.getBeat()

		if this_beat > self.last_oscillation_beat:
			self.last_oscillation_beat = this_beat
			self.first_color = not self.first_color

		next_beat = self.current_song.getSecondsToNextBeat()

		last_beat = self.current_song.getSecondsSinceBeat()

		lum_ratio = min(max((next_beat ** 2) / ((next_beat + last_beat) ** 2) / 2, 0), 1)

		color_ratio = lum_ratio  # next_beat / ((last_beat + next_beat) / 2)
		if color_ratio > 0.5:
			color_ratio = 1 - ((1 - color_ratio) ** 2)
		else:
			color_ratio = color_ratio ** 2

		if self.first_color:
			self.color.red = (color_ratio * self.oscillation_colors[0].red) + ((1 - color_ratio) *
			                                                                   self.oscillation_colors[1].red)
			self.color.green = (color_ratio * self.oscillation_colors[0].green) + ((1 - color_ratio) *
			                                                                       self.oscillation_colors[1].green)
			self.color.blue = (color_ratio * self.oscillation_colors[0].blue) + ((1 - color_ratio) *
			                                                                     self.oscillation_colors[1].blue)
		else:
			self.color.red = ((1 - color_ratio) * self.oscillation_colors[0].red) + (
						color_ratio * self.oscillation_colors[1].red)
			self.color.green = ((1 - color_ratio) * self.oscillation_colors[0].green) + (
					color_ratio * self.oscillation_colors[1].green)
			self.color.blue = ((1 - color_ratio) * self.oscillation_colors[0].blue) + (
					color_ratio * self.oscillation_colors[1].blue)

		self.color = setValue(self.color, max(0, min(lum_ratio + 0.05, 1)))

	def getColor(self):
		return self.color

	def processSongChange(self):
		self.last_oscillation_beat = 0
		self.first_color = True
		if self.first_color:
			self.color = self.oscillation_colors[0]
		else:
			self.color = self.oscillation_colors[1]
