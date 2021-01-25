from colour import Color

from patterns2.pattern import pattern

class three_color_oscillation_1(pattern):

	@staticmethod
	def isDisco():
		return False

	@staticmethod
	def getName():
		return "three_color_oscillation_1"

	def __init__(self, now_playing):
		self.current_song = now_playing
		self.oscillation_colors = [Color('#4b7fd1'), Color('#d64945'), Color('#edc121')]
		self.color_indice = 0
		self.oscillation_color = self.oscillation_colors[self.color_indice]
		self.last_oscillation_beat = 0

	def iterate(self):

		this_beat = self.current_song.getBeat()

		if this_beat > self.last_oscillation_beat:
			self.last_oscillation_beat = this_beat
			self.color_indice += 1
			if self.color_indice > len(self.oscillation_colors) - 1:
				self.color_indice = 0

		next_beat = self.current_song.getSecondsToNextBeat()

		last_beat = self.current_song.getSecondsSinceBeat()

		lum_ratio = min(max((next_beat ** 2) / ((next_beat + last_beat) ** 2) / 2, 0), 1)

		color_ratio = lum_ratio  # next_beat / ((last_beat + next_beat) / 2)
		if color_ratio > 0.5:
			color_ratio = 1 - ((1 - color_ratio) ** 2)
		else:
			color_ratio = color_ratio ** 2

		last_color_indice = self.color_indice - 1
		if last_color_indice < 0:
			last_color_indice = len(self.oscillation_colors) - 1
		self.oscillation_color.red = (color_ratio * self.oscillation_colors[self.color_indice].red) + ((1 - color_ratio) *
		                                                                                               self.oscillation_colors[
			                                                                                               last_color_indice].red)
		self.oscillation_color.green = (color_ratio * self.oscillation_colors[self.color_indice].green) + ((1 - color_ratio) *
		                                                                                                   self.oscillation_colors[
			                                                                                                   last_color_indice].green)
		self.oscillation_color.blue = (color_ratio * self.oscillation_colors[self.color_indice].blue) + ((1 - color_ratio) *
		                                                                                                 self.oscillation_colors[
			                                                                                                 last_color_indice].blue)


		self.oscillation_color = self.setValue(self.oscillation_color, max(0, min(lum_ratio + 0.05, 1)))

	def getColor(self):
		return self.oscillation_color

	def processSongChange(self):
		self.last_oscillation_beat = 0
		self.color_indice = 0
		self.oscillation_color = self.oscillation_colors[self.color_indice]
