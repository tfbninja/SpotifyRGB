from colour import Color

from patterns2.pattern import pattern
#from SpotifyLiaison import setValue, getDiscoBar


class police_disco(pattern):

	@staticmethod
	def isDisco():
		return True

	@staticmethod
	def getName():
		return "police_disco"

	def __init__(self, now_playing):
		self.current_song = now_playing
		self.hues = [Color("Red"), Color("Blue"), Color("White")]
		self.modes = ["11123", "RRRBWBBBRW"]
		self.current_mode = 0
		self.color = self.hues[0]
		self.disco_bar = 0.040  # in seconds (40 millis)

	def iterate(self):
		this_beat = self.current_song.getBeat()
		match self.current_mode:
			case 0:
				pass
			case 1:
				pass
			case 2:
				pass
			case _:
				pass

		if this_beat > self.last_disco_beat + 1:  # change hues every other beat
			self.last_disco_beat = this_beat
			self.current_mode += 1
			if self.current_mode > len(self.hues) - 1:
				self.current_mode = 0
		self.color = self.hues[self.current_mode]

		next_tatum = self.current_song.getSecondsToNextTatum()

		last_tatum = self.current_song.getSecondsSinceTatum()

		if (next_tatum <= self.disco_bar / 2) or (last_tatum <= self.disco_bar / 2):
			self.color = self.setValue(self.color, 1)
		else:
			self.color = self.setValue(self.color, 0.01)

	def getColor(self):
		return self.color

	def processSongChange(self):
		self.current_mode = 0
		self.color = self.current_mode
		self.last_disco_beat = 0
