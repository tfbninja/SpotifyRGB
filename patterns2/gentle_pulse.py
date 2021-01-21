from colour import Color
from SpotifyLiaison import setValue
import pattern

def isDisco():
	return False

def utilizesRandom():
	return False

def getName():
	return "gentle_pulse"

class gentle_pulse(pattern):

	def __init__(self, now_playing):
		self.current_song = now_playing
		self.color = Color("Blue")

	def iterate(self):
		if self.color.hue < 0.998:
			self.color.hue = self.color.hue + 0.0005
		else:
			self.color.hue = 0

		next_beat = self.current_song.getSecondsToNextBeat()

		last_beat = self.current_song.getSecondsSinceBeat()

		ratio = (0.2 * (next_beat / (next_beat + last_beat))) ** 0.8

		self.color = setValue(self.color, ratio)

	def getColor(self):
		return self.color

	def processSongChange(self):
		# no need to do anything for this function :)
		pass
