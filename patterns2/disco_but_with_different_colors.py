from colour import Color

from patterns2.pattern import pattern


class disco_but_with_different_colors(pattern):

	@staticmethod
	def isDisco():
		return True

	@staticmethod
	def getName():
		return "disco_but_with_different_colors"

	def __init__(self, now_playing):
		self.current_song = now_playing
		self.hues = [Color('#4ec7c1'), Color('#8715a3'), Color('#d6a727'), Color('#8a0615')]
		self.current_hue = 0
		self.color = self.hues[self.current_hue]
		self.last_disco_beat = 0
		self.disco_bar = 0.050  # in seconds (50 millis)

	def iterate(self):

		# change hues every other beat
		this_beat = self.current_song.getBeat()
		if  this_beat > self.last_disco_beat + 1:
			self.last_disco_beat = this_beat
			self.current_hue += 1
			if self.current_hue > len(self.hues) - 1:
				self.current_hue = 0
		self.color = self.hues[self.current_hue]

		next_tatum = self.current_song.getSecondsToNextTatum()

		last_tatum = self.current_song.getSecondsSinceTatum()

		disco_bar = self.disco_bar

		# basically we turn the lights on at full blast for disco_bar length in seconds centered at the tatum's time
		if next_tatum <= disco_bar / 2 or last_tatum <= disco_bar / 2:
			self.color = self.setValue(self.color, 1)
		else:
			self.color = self.setValue(self.color, 0.01)

	def getColor(self):
		return self.color

	def processSongChange(self):
		self.current_hue = 0
		self.color = self.current_hue
		self.last_disco_beat = 0
