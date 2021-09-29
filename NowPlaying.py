import sys
import time
# import Threading #later
# test
from math import floor

class NowPlaying:
	def __init__(self, sp):
		self.sp = sp
		self.retry_attempts = 3
		self.retry_wait_time_millis = 250
		self.resync_index = 0
		self.results = self.sp.current_user_playing_track()

		self.is_playing = self.results['is_playing']
		if self.is_playing:
			self.progress_ms = self.results['progress_ms']
			self.ms_start = time.time()

			self.name = self.results['item']['name']
			self.uri = self.results['item']['uri']
			self.song_length = self.results['item']['duration_ms']

			self.analysis = self.sp.audio_analysis(self.uri)
			self.section_list = self.analysis['sections']
			self.beat_list = self.analysis['beats']
			self.tatum_list = self.analysis['tatums']

			for i in range(len(self.section_list)):
				self.section_list[i]['start'] = round(self.section_list[i]['start'], 4)
			for i in range(len(self.beat_list)):
				self.beat_list[i]['start'] = round(self.beat_list[i]['start'], 4)
			for i in range(len(self.tatum_list)):
				self.tatum_list[i]['start'] = round(self.tatum_list[i]['start'], 4)
			self.features = self.sp.audio_features(self.uri)
			# self.tempo = self.features[0]['tempo']
			self.time_signature = self.features[0]['time_signature']

	def reSync(self):
		print("re-syncing " + str(self.resync_index))
		self.resync_index += 1
		tempResults = self.sp.current_user_playing_track()
		self.is_playing = tempResults['is_playing']
		if self.is_playing:
			if self.uri != tempResults['item']['uri']:
				self.results = self.sp.current_user_playing_track()

				self.is_playing = self.results['is_playing']
				if self.is_playing:
					self.progress_ms = self.results['progress_ms']
					self.ms_start = time.time()

					self.name = self.results['item']['name']
					self.uri = self.results['item']['uri']
					self.song_length = self.results['item']['duration_ms']

					self.analysis = self.sp.audio_analysis(self.uri)
					self.section_list = self.analysis['sections']
					self.beat_list = self.analysis['beats']
					self.tatum_list = self.analysis['tatums']

					for i in range(len(self.section_list)):
						self.section_list[i]['start'] = round(self.section_list[i]['start'], 4)
					for i in range(len(self.beat_list)):
						self.beat_list[i]['start'] = round(self.beat_list[i]['start'], 4)
					for i in range(len(self.tatum_list)):
						self.tatum_list[i]['start'] = round(self.tatum_list[i]['start'], 4)
					self.features = self.sp.audio_features(self.uri)
					# self.tempo = self.features[0]['tempo']
					self.time_signature = self.features[0]['time_signature']
					print("sync successful")
					return True
				return
			self.progress_ms = tempResults['progress_ms']
			self.ms_start = time.time()
			self.is_playing = tempResults['is_playing']
			print("sync successful")
			return True

	def hardReSync(self):
		print("hard re-syncing " + str(self.resync_index))
		self.resync_index += 1
		tempResults = self.sp.current_user_playing_track()
		self.is_playing = tempResults['is_playing']

		#self.results = self.sp.current_user_playing_track()
		self.results = tempResults

		self.is_playing = self.results['is_playing']
		self.progress_ms = self.results['progress_ms']
		self.ms_start = time.time()

		self.name = self.results['item']['name']
		self.uri = self.results['item']['uri']
		self.song_length = self.results['item']['duration_ms']

		self.analysis = self.sp.audio_analysis(self.uri)
		self.section_list = self.analysis['sections']
		self.beat_list = self.analysis['beats']
		self.tatum_list = self.analysis['tatums']

		for i in range(len(self.section_list)):
			self.section_list[i]['start'] = round(self.section_list[i]['start'], 4)
		for i in range(len(self.beat_list)):
			self.beat_list[i]['start'] = round(self.beat_list[i]['start'], 4)
		for i in range(len(self.tatum_list)):
			self.tatum_list[i]['start'] = round(self.tatum_list[i]['start'], 4)
		self.features = self.sp.audio_features(self.uri)
		# self.tempo = self.features[0]['tempo']
		self.time_signature = self.features[0]['time_signature']
		print("hard sync successful, song name: " + self.name)
		return True

	def getSectionList(self):
		return self.section_list

	def getBeatList(self):
		return self.beat_list

	def getTatumList(self):
		return self.tatum_list

	def getPosInSongMillis(self):
		deltaMS = (time.time() - self.ms_start) * 1000
		return deltaMS + self.progress_ms

	def getName(self):
		return self.name

	def getURI(self):
		return self.uri

	"""
	def getTempo(self):
		return self.tempo
	"""

	def getTimeSignature(self):
		return self.time_signature

	def getSongLengthMillis(self):
		return self.song_length

	def isPlaying(self):
		if self.is_playing:  # this is in case it's undefined or whatever
			return self.is_playing
		else:
			return False

	def roundTo4(num):
		return round(num, 4)

	def getSecondsToNextSection(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for sectionIndice in range(len(self.section_list) - 2, 0, -1):
				if time_seconds > self.section_list[sectionIndice]['start']:
					return self.section_list[sectionIndice + 1]['start'] - time_seconds
			self.timeoutSleep(i)
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get seconds to next section.").with_traceback(tb)

	def getSecondsSinceSection(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for sectionIndice in range(len(self.section_list) - 2, 0, -1):
				if time_seconds > self.section_list[sectionIndice]['start']:
					return time_seconds - self.section_list[sectionIndice]['start']
			self.timeoutSleep(i)
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get seconds since section.").with_traceback(tb)

	def getSection(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for sectionIndex in range(len(self.section_list) - 2, 0, -1):
				if time_seconds > self.section_list[sectionIndex]['start']:
					return sectionIndex
			self.timeoutSleep(i)
			print("Retrying Section")
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get section.").with_traceback(tb)

	def getSecondsToNextBeat(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for beatIndice in range(len(self.beat_list) - 2, 0, -1):
				if time_seconds > self.beat_list[beatIndice]['start']:
					return self.beat_list[beatIndice + 1]['start'] - time_seconds
			self.timeoutSleep(i)
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get seconds to next beat.").with_traceback(tb)

	def getSecondsToNthBeat(self, n):
		if n < len(self.beat_list):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for i in range(self.retry_attempts):
				for beatIndice in range(len(self.beat_list) - (1 + n), 0, -1):
					if time_seconds > self.beat_list[beatIndice]['start']:
						return self.beat_list[beatIndice + n]['start'] - time_seconds
				self.timeoutSleep(i)
				self.reSync()
			self.hardReSync()
			tb = sys.exc_info()[2]
			raise Exception("Could not get seconds to nth beat.").with_traceback(tb)
		print("not enough beats to calculate nth")
		return n

	def getSecondsSinceBeat(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for beatIndice in range(len(self.beat_list) - 2, 0, -1):
				if time_seconds > self.beat_list[beatIndice]['start']:
					return time_seconds - self.beat_list[beatIndice]['start']
			self.timeoutSleep(i)
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get seconds since beat.").with_traceback(tb)

	def getBeat(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			if millis > millis / 2:
				for beatIndice in range(len(self.beat_list) - 2, 0, -1):
					if time_seconds > self.beat_list[beatIndice]['start']:
						return beatIndice
			else:
				for beatIndice in range(0, len(self.beat_list) - 2):
					if time_seconds < self.beat_list[beatIndice]['start']:
						return beatIndice - 1
			self.timeoutSleep(i)
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get beat.").with_traceback(tb)

	def getSecondsToNextTatum(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for tatumIndice in range(len(self.tatum_list) - 2, 0, -1):
				if time_seconds > self.tatum_list[tatumIndice]['start']:
					return self.tatum_list[tatumIndice + 1]['start'] - time_seconds
			self.timeoutSleep(i)
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get seconds to next tatum.").with_traceback(tb)

	def getSecondsToNthTatum(self, n):
		if n < len(self.tatum_list):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for i in range(self.retry_attempts):
				for tatumIndice in range(len(self.tatum_list) - (1 + n), 0, -1):
					if time_seconds > self.tatum_list[tatumIndice]['start']:
						return self.tatum_list[tatumIndice + n]['start'] - time_seconds
				self.timeoutSleep(i)
				self.reSync()
			self.hardReSync()
			tb = sys.exc_info()[2]
			raise Exception("Could not get seconds to nth tatum.").with_traceback(tb)
		print("not enough tatums to calculate nth")
		return 0.1

	def getSecondsSinceTatum(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for tatumIndice in range(len(self.tatum_list) - 2, 0, -1):
				if time_seconds > self.tatum_list[tatumIndice]['start']:
					return time_seconds - self.tatum_list[tatumIndice]['start']
			self.timeoutSleep(i)
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get seconds since tatum.").with_traceback(tb)

	def getTatum(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			if millis > self.getSongLengthMillis() / 2:
				for tatumIndice in range(len(self.tatum_list) - 2, 0, -1):
					if time_seconds > self.tatum_list[tatumIndice]['start']:
						return tatumIndice
			else:
				for tatumIndice in range(0, len(self.tatum_list) - 2):
					if time_seconds < self.tatum_list[tatumIndice]['start']:
						return tatumIndice - 1
			self.timeoutSleep(i)
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get tatum.").with_traceback(tb)

	def timeoutSleep(self, iteration):
		for i in range(floor(self.retry_wait_time_millis * (1.2 * iteration))):
			time.sleep(0.001)
		return
