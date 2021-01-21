from colour import Color
from SpotifyLiaison import setValue
import pattern

def isDisco():
	return False

def utilizesRandom():
	return False

def getName():
	return "time_signature_pulse"

class time_signature_pulse(pattern):

	def __init__(self, now_playing):
		self.current_song = now_playing
		self.color = Color("#44f25b")
		self.hue_add = 0.31
		self.indice = 0
		self.last_tatum_no = 0
		self.time_signature = now_playing.getTimeSignature()

	def iterate(self):
		if self.indice == self.time_signature:
			self.indice = 0
			self.color.hue += self.hue_add
			self.color.hue = self.color.hue % 1

		next_tatum = self.current_song.getSecondsToNextTatum()

		last_tatum = self.current_song.getSecondsSinceTatum()

		ratio = (next_tatum ** 2) / (next_tatum + last_tatum ** 2)

		this_tatum = self.current_song.getTatum()
		if this_tatum > self.last_tatum_no:
			self.last_tatum_no = this_tatum
			self.indice += 1

		self.color = setValue(self.color, ratio + 0.05)

	def getColor(self):
		return self.color

	def processSongChange(self):
		self.indice = 0
		self.last_tatum_no = 0
		self.time_signature = self.current_song.getTimeSignature()
