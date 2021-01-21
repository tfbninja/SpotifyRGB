from colour import Color
import pattern

def isDisco():
	return False

def utilizesRandom():
	return False

def getName():
	return "basic_hue_change"

class basic_hue_change(pattern):

	def __init__(self):
		self.color = Color("Red")
		self.hue_increment = 0.001

	def iterate(self):
		if self.color.hue < 1 - self.hue_increment:
			self.color.hue += self.hue_increment
		else:
			self.color.hue = 0

	def getColor(self):
		return self.color

	def processSongChange(self):
		# no need to do anything for this function :)
		pass
