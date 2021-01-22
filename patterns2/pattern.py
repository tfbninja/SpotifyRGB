from abc import ABC, abstractmethod
import colorsys  # see colour import for why i need to import TWO color libraries
from colour import Color  # WHY NO HSV SUPPORT C'MON (literal rage but at the same time i get it)
import random

class pattern(ABC):

	@staticmethod
	@abstractmethod
	def isDisco(self):
		pass

	@staticmethod
	@abstractmethod
	def getName(self):
		pass

	@abstractmethod
	def __init__(self):
		pass

	@abstractmethod
	def processSongChange(self):
		pass

	@abstractmethod
	def iterate(self):
		pass

	@abstractmethod
	def getColor(self):
		pass

	@classmethod
	def setValue(cls, color, val):
		oldColor = colorsys.rgb_to_hsv(color.red, color.green, color.blue)
		output = Color(rgb=colorsys.hsv_to_rgb(oldColor[0], oldColor[1], val))
		return output

	@classmethod
	def randomishColor(cls):
		total = random.randint(0, 255 * 3)
		random1 = random.randint(0, min(255, total))
		random2 = random.randint(0, min(255, total - random1))
		random3 = random.randint(0, min(255, total - (random1 + random2)))
		randoms = [float(random1), float(random2), float(random3)]
		random.shuffle(randoms)
		outColor = Color(rgb=(randoms[0] / 256, randoms[1] / 256, randoms[2] / 256))
		return outColor
