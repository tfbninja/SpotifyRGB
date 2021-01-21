from colour import Color
from SpotifyLiaison import setValue
import random
import pattern

def isDisco():
	return False

def utilizesRandom():
	return True

def getName():
	return "rand_color_swirl"

class rand_color_swirl(pattern):

	def __init__(self, now_playing):
		self.current_song = now_playing
		self.color = Color("Blue")
		self.pulse_baseline = 0.3
		self.random = random.random()

	def iterate(self):
		if self.color.hue < 0.998:
			self.color.hue = self.color.hue + self.random.randint(-1, 5) / 10000
		else:
			self.color.hue = 0

		nextBeat = self.current_song.getSecondsToNextBeat()
		lastBeat = self.current_song.getSecondsSinceBeat()

		ratio = (nextBeat ** 2) / (nextBeat + lastBeat ** 2)

		self.color = setValue(self.color, min(ratio + 0.05, 1))

	def getColor(self):
		return self.color

	def newRandomSeed(self, seed):
		print("old random seed in rand_color_swirl.py: " + str(self.random.seed))
		self.random.seed = seed
		print("what the new seed should be: " + str(seed) + ", what is actually is: " + str(self.random.seed))

	def processSongChange(self):
		# no need to do anything for this function :)
		newRandomSeed(self.random.randint(0, 1023)) # just cuz I can *shrug*
