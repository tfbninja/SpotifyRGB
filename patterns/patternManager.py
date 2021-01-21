import random
class pattern_manager():

	def __init__(self, now_playing, pattern_list, current_pattern, discos_per_song, discos_done):
		self.current_song = now_playing
		self.pattern_list = pattern_list
		self.non_disco_patterns = []
		for pattern in pattern_list:
			if not pattern.isDisco():
				self.non_disco_patterns.append(pattern[1])

		self.current_pattern = pattern_list[current_pattern]
		self.discos_per_song = discos_per_song
		self.discos_done = discos_done

	def iteratePatternColor(self):
		self.current_pattern.iterate()

	def getPatternColor(self):
		return self.currentPattern.getColor()

	def getPatternName(self):
		self.current_pattern.getName()

	def nextRandomPattern(self):
		successful = False

		# You don't want the lights doing too many disco patterns, so we make sure we haven't done more than the
		# allowed amount, also you probably don't want a disco at the beginning of the song
		can_be_disco = self.discos_done < self.discos_per_song and not self.current_song.getSection() == 0

		valid_choices = []
		if can_be_disco:
			valid_choices = [*range(len(self.pattern_list))]
			valid_choices.remove(self.current_pattern)
		else:
			valid_choices = self.non_disco_patterns
		self.current_pattern = random.choice(valid_choices)

	def processSongChange(self):
		self.discos_done = 0
		self.nextRandomPattern()
		for pattern in self.pattern_list:
			pattern.processSongChanged()
			if pattern.utilizesRandom():
				pattern.newRandomSeed()
