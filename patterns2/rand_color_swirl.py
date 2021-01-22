import random

from colour import Color

from patterns2.pattern import pattern


class rand_color_swirl(pattern):

	@staticmethod
	def isDisco():
		return False

	@staticmethod
	def getName():
		return "rand_color_swirl"

	def __init__(self, now_playing):
		self.current_song = now_playing
		self.color = Color("Blue")
		self.pulse_baseline = 0.3

	def iterate(self):
		if self.color.hue < 0.998:
			self.color.hue = self.color.hue + random.randint(-1, 5) / 10000
		else:
			self.color.hue = 0

		nextBeat = self.current_song.getSecondsToNextBeat()
		lastBeat = self.current_song.getSecondsSinceBeat()

		ratio = (nextBeat ** 2) / (nextBeat + lastBeat ** 2)

		self.color = self.setValue(self.color, min(ratio + 0.05, 1))

	def getColor(self):
		return self.color

	def processSongChange(self):
		# no need to do anything for this function :)
		pass
