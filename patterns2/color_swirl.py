from colour import Color

from patterns2.pattern import pattern

class color_swirl(pattern):

	@staticmethod
	def isDisco():
		return False

	@staticmethod
	def getName():
		return "color_swirl"

	def __init__(self, now_playing):
		self.current_song = now_playing
		self.starting_color = Color("Blue")
		self.color = self.starting_color
		self.pulse_baseline = 0.3

	def iterate(self):
		if self.color.hue < 0.998:
			self.color.hue = self.color.hue + 0.0005
		else:
			self.color.hue = 0

		nextBeat = self.current_song.getSecondsToNextBeat()
		lastBeat = self.current_song.getSecondsSinceBeat()

		# this ratio is the ratio of how far along in the beat we are, if its right before the next beat
		# it should be near 1. if we just had a beat, it should be near 0
		ratio = nextBeat / ((nextBeat + lastBeat) / 2) * (1 - self.pulse_baseline) + self.pulse_baseline

		# to get a pulsing effect, we apply the ratio calculated earlier to the value level of the color we've already assigned
		self.color = self.setValue(self.color, max(min(ratio, 1), 0))

	def getColor(self):
		return self.color

	def processSongChange(self):
		self.color = self.starting_color
