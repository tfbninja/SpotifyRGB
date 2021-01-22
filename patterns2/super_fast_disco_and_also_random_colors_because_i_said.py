import random
from patterns2.pattern import pattern

class super_fast_disco_and_also_random_colors_because_i_said(pattern):

	@staticmethod
	def isDisco():
		return True

	@staticmethod
	def getName():
		return "super_fast_disco_and_also_random_colors_because_i_said"

	def __init__(self, now_playing):
		self.current_song = now_playing
		self.hues = [self.randomishColor(), self.randomishColor(), self.randomishColor(), self.randomishColor()]
		self.current_hue = 0
		self.color = self.hues[self.current_hue]
		self.last_disco_beat = 0
		self.disco_bar = 0.050  # in seconds (40 millis)

	def iterate(self):
		this_beat = self.current_song.getBeat()
		if this_beat > self.last_disco_beat + 1:  # change hues every other beat
			self.last_disco_beat = this_beat
			self.current_hue += 1
			if self.current_hue > len(self.hues) - 1:
				self.current_hue = 0
		self.color = self.hues[self.current_hue]

		next_tatum = self.current_song.getSecondsToNextTatum()

		last_tatum = self.current_song.getSecondsSinceTatum()

		if next_tatum <= self.disco_bar / 2 or last_tatum <= self.disco_bar / 2:
			self.color = self.setValue(self.color, 1)
		else:
			self.color = self.setValue(self.color, 0.01)

	def setDiscoBar(self, amtInSeconds):
		self.disco_bar = amtInSeconds

	def getColor(self):
		return self.color

	def processSongChange(self):
		self.current_hue = 0
		self.color = self.current_hue
		self.last_disco_beat = 0
