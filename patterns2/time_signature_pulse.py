from colour import Color

from patterns2.pattern import pattern

class time_signature_pulse(pattern):

	@staticmethod
	def isDisco():
		return False

	@staticmethod
	def getName():
		return "time_signature_pulse"

	def __init__(self, now_playing):
		self.current_song = now_playing
		self.color = Color("#44f25b")
		self.hue_add = 0.31
		self.index = self.current_song.getBeat() % 4
		self.last_tatum_no = 0
		self.time_signature = now_playing.getTimeSignature()

	def iterate(self):
		if self.index == self.time_signature:
			self.index = 0
			self.color.hue += self.hue_add
			self.color.hue = self.color.hue % 1

		next_tatum = self.current_song.getSecondsToNextTatum()

		last_tatum = self.current_song.getSecondsSinceTatum()

		ratio = max(min((next_tatum ** 2) / (next_tatum + last_tatum ** 2), 1), 0)

		this_tatum = self.current_song.getTatum()
		if this_tatum > self.last_tatum_no:
			self.last_tatum_no = this_tatum
			self.index += 1

		self.color = self.setValue(self.color, max(min(ratio + 0.05, 1),0))

	def getColor(self):
		return self.color

	def processSongChange(self):
		self.index = self.current_song.getBeat() % 4
		self.last_tatum_no = 0
		self.time_signature = self.current_song.getTimeSignature()
