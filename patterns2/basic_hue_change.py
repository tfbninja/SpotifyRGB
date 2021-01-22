from colour import Color

from patterns2.pattern import pattern

class basic_hue_change(pattern):

	@staticmethod
	def isDisco():
		return False

	@staticmethod
	def getName():
		return "basic_hue_change"

	# now_playing can be null, doesn't matter. only added so that all patterns have same init variables
	def __init__(self, now_playing):
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
