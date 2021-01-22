import random

import patterns2

class patternManager:

	def dynamicImportClassFromPatterns2(self, class_name):
		# tysm to the user who posted these two slightly modified lines at
		# https://stackoverflow.com/a/547867/8079326
		mod = __import__('patterns2.' + class_name, fromlist=[class_name])
		klass = getattr(mod, class_name)
		return klass

	def __init__(self, now_playing, pattern_list, start_pattern, discos_per_song, discos_done):
		self.current_song = now_playing
		self.pattern_list = []
		self.pattern_names_list = []
		self.non_disco_patterns = []
		if len(pattern_list) == 0:

			# FIXME
			# gotta import all patterns in dir
			# also have to assign self.pattern_list
			print("No patterns specified, importing all: " + str(patterns2.__all__))
			for pattern_name in patterns2.__all__:
				pattern = self.dynamicImportClassFromPatterns2(pattern_name) # take a look at this function :)
				self.pattern_list.append(pattern(self.current_song))
				self.pattern_names_list.append(pattern.getName())
				if not pattern.isDisco():
					self.non_disco_patterns.append(pattern)
		else:
			print("Importing only these patterns: " + str(pattern_list))
			for pattern_name in pattern_list:
				pattern = self.dynamicImportClassFromPatterns2(pattern_name)  # take a look at this function :)
				self.pattern_list.append(pattern(self.current_song))
				self.pattern_names_list.append(pattern.getName())
				if not pattern.isDisco():
					self.non_disco_patterns.append(pattern)

		print("successfully imported the following patterns: " + str(self.pattern_list))
		self.current_pattern = self.pattern_list[start_pattern]#(self.current_song)
		self.discos_per_song = discos_per_song
		self.discos_done = discos_done

	def iteratePatternColor(self):
		self.current_pattern.iterate()

	def getPatternColor(self):
		return self.current_pattern.getColor()

	def getPatternName(self):
		return self.current_pattern.getName()

	def nextRandomPattern(self):
		# You don't want the lights doing too many disco patterns, so we make sure we haven't done more than the
		# allowed amount, also you probably don't want a disco at the beginning of the song
		can_be_disco = self.discos_done < self.discos_per_song and not self.current_song.getSection() == 0

		if can_be_disco:
			valid_choices = [*range(len(self.pattern_list))]
			valid_choices.pop(self.pattern_names_list.index(self.current_pattern.getName()))
		else:
			valid_choices = self.non_disco_patterns
		self.current_pattern = self.pattern_list[random.choice(valid_choices)]#(self.current_song)

	def nextPattern(self, pattern_n):
		#don't restart the pattern if it's the same
		if self.pattern_list[self.pattern_names_list.index(pattern_n)].getName() != self.current_pattern.getName():
			self.current_pattern = self.pattern_list[self.pattern_names_list.index(pattern_n)]

	def processSongChange(self):
		self.discos_done = 0
		self.nextRandomPattern()
		for pattern in self.pattern_list:
			pattern.processSongChange()
