from colour import Color
from SpotifyLiaison import setValue, getDiscoBar
import pattern

def isDisco():
	return True

def utilizesRandom():
	return False

def getName():
	return "disco_but_with_different_colors"

class disco_but_with_different_colors(pattern):

	def __init__(self, now_playing):
		self.current_song = now_playing
		self.hues = [Color("Red"), Color("Blue"), Color("White")]
		self.current_hue = self.hues[0]
		self.color = self.current_hue
		self.last_disco_beat = 0

	def iterate(self):

		disco_color_hues = [Color('#4ec7c1'), Color('#8715a3'), Color('#d6a727'), Color('#8a0615')]

		# change hues every other beat
		this_beat = self.current_song.getBeat()
		if  this_beat > self.last_disco_beat + 1:
			self.last_disco_beat = this_beat
			self.current_hue += 1
			if self.current_hue > len(disco_color_hues) - 1:
				self.current_hue = 0
		self.color = disco_color_hues[self.current_hue]

		next_tatum = self.current_song.getSecondsToNextTatum()

		last_tatum = self.current_song.getSecondsSinceTatum()

		disco_bar = getDiscoBar()

		# basically we turn the lights on at full blast for disco_bar length in seconds centered at the tatum's time
		if next_tatum <= disco_bar / 2 or last_tatum <= disco_bar / 2:
			self.color = setValue(self.color, 1)
		else:
			self.color = setValue(self.color, 0.01)

	def getColor(self):
		return self.color

	def processSongChange(self):
		self.current_hue = self.hues[0]
		self.color = self.current_hue
		self.last_disco_beat = 0
