from colour import Color
import random
from SpotifyLiaison import setValue, getDiscoBar, randomishColorSeed
import pattern

def isDisco():
	return True

def utilizesRandom():
	return True

def getName():
	return "super_fast_disco_and_also_random_colors_because_i_said"

class super_fast_disco_and_also_random_colors_because_i_said(pattern):

	def __init__(self, now_playing):
		self.current_song = now_playing
		self.random = random.random()
		self.hues = [randomishColorSeed(self.random.seed), randomishColorSeed(self.random.seed), randomishColorSeed(
			self.random.seed), randomishColorSeed(
			self.random.seed)]
		self.current_hue = self.hues[0]
		self.color = self.current_hue
		self.last_disco_beat = 0

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

		disco_bar = getDiscoBar()
		if next_tatum <= disco_bar / 2 or last_tatum <= disco_bar / 2:
			self.color = setValue(self.color, 1)
		else:
			self.color = setValue(self.color, 0.01)

	def getColor(self):
		return self.color

	def newRandomSeed(self, seed):
		print("old random seed in rand_color_swirl.py: " + str(self.random.seed))
		self.random.seed = seed
		print("what the new seed should be: " + str(seed) + ", what is actually is: " + str(self.random.seed))

	def processSongChange(self):
		self.current_hue = self.hues[0]
		self.color = self.current_hue
		self.last_disco_beat = 0
