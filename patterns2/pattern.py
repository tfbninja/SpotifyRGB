from abc import ABC

class pattern(ABC):

	@abstractmethod
	def isDisco(self):
		pass

	@abstractmethod
	def utilizesRandom(self):
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

	@abstractmethod
	def getName(self):
		pass

