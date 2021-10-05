import sys
import time
# import Threading #later
# test
from math import floor

import requests


def roundTo4(num):
	return round(num, 4)


class NowPlaying:
	def __init__(self, sp):
		self.sp = sp
		self.retry_attempts = 10
		self.retry_wait_time_millis = 250
		self.resync_index = 0
		self.results = []
		self.is_playing = False
		self.progress_ms = 0
		self.ms_start = 0

		self.name = ""
		self.uri = ""
		self.song_length = 0

		self.analysis = []
		self.section_list = []
		self.bar_list = []
		self.beat_list = []
		self.tatum_list = []
		self.hardReSync()

	def reSync(self):
		print("re-syncing " + str(self.resync_index))
		self.resync_index += 1

		tempResults = 0
		for i in range(self.retry_attempts):
			try:
				tempResults = self.sp.current_user_playing_track()
				break
			except requests.exceptions.ReadTimeout:
				time.sleep(self.retry_wait_time_millis * i * 1.2)
		return self.softParseResults(tempResults)

	def hardReSync(self):
		print("hard re-syncing " + str(self.resync_index))
		self.resync_index += 1
		tempResults = 0
		for i in range(self.retry_attempts):
			try:
				tempResults = self.sp.current_user_playing_track()
				break
			except requests.exceptions.ReadTimeout:
				time.sleep(self.retry_wait_time_millis * i * 1.2)
		return self.parseAllResults(tempResults)

	def parseAllResults(self, results):
		self.is_playing = results['is_playing']
		if self.is_playing:
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
				self.bar_list = self.analysis['bars']
				self.beat_list = self.analysis['beats']
				self.tatum_list = self.analysis['tatums']

				for i in range(len(self.section_list)):
					self.section_list[i]['start'] = round(self.section_list[i]['start'], 4)
				for i in range(len(self.bar_list)):
					self.bar_list[i]['start'] = round(self.bar_list[i]['start'], 4)
				for i in range(len(self.beat_list)):
					self.beat_list[i]['start'] = round(self.beat_list[i]['start'], 4)
				for i in range(len(self.tatum_list)):
					self.tatum_list[i]['start'] = round(self.tatum_list[i]['start'], 4)
				self.features = self.sp.audio_features(self.uri)
				self.time_signature = self.features[0]['time_signature']
				return True

	def softParseResults(self, results):
		self.is_playing = results['is_playing']
		if self.is_playing:
			if self.uri != results['item']['uri']:
				return self.parseAllResults(results)
			self.progress_ms = results['progress_ms']
			self.ms_start = time.time()

	def getSectionList(self):
		return self.section_list

	def getBarList(self):
		return self.bar_list

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

	def getSecondsToNextSection(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for sectionIndex in range(len(self.section_list) - 2, 0, -1):
				if time_seconds > self.section_list[sectionIndex]['start']:
					return self.section_list[sectionIndex + 1]['start'] - time_seconds
			self.timeoutSleep(i)
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get seconds to next section.").with_traceback(tb)

	def getSecondsSinceSection(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for sectionIndex in range(len(self.section_list) - 2, 0, -1):
				if time_seconds > self.section_list[sectionIndex]['start']:
					return time_seconds - self.section_list[sectionIndex]['start']
			self.timeoutSleep(i)
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get seconds since section.").with_traceback(tb)

	def getBar(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for barIndex in range(len(self.bar_list) - 2, 0, -1):
				if time_seconds > self.bar_list[barIndex]['start']:
					return barIndex
			self.timeoutSleep(i)
			print("Retrying getBar")
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get bar.").with_traceback(tb)

	def getSecondsToNextBar(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for barIndex in range(len(self.bar_list) - 2, 0, -1):
				if time_seconds > self.bar_list[barIndex]['start']:
					return self.bar_list[barIndex + 1]['start'] - time_seconds
			self.timeoutSleep(i)
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get seconds to next bar.").with_traceback(tb)

	def getSecondsSinceBar(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for barIndex in range(len(self.bar_list) - 2, 0, -1):
				if time_seconds > self.bar_list[barIndex]['start']:
					return time_seconds - self.bar_list[barIndex]['start']
			self.timeoutSleep(i)
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get seconds since bar.").with_traceback(tb)

	def getBeat(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			if millis > millis / 2:
				for beatIndex in range(len(self.beat_list) - 2, 0, -1):
					if time_seconds > self.beat_list[beatIndex]['start']:
						return beatIndex
			else:
				for beatIndex in range(0, len(self.beat_list) - 2):
					if time_seconds < self.beat_list[beatIndex]['start']:
						return beatIndex - 1
			self.timeoutSleep(i)
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get beat.").with_traceback(tb)

	def getSecondsToNextBeat(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for beatIndex in range(len(self.beat_list) - 2, 0, -1):
				if time_seconds > self.beat_list[beatIndex]['start']:
					return self.beat_list[beatIndex + 1]['start'] - time_seconds
			self.timeoutSleep(i)
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get seconds to next beat.").with_traceback(tb)

	def getSecondsSinceBeat(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for beatIndex in range(len(self.beat_list) - 2, 0, -1):
				if time_seconds > self.beat_list[beatIndex]['start']:
					return time_seconds - self.beat_list[beatIndex]['start']
			self.timeoutSleep(i)
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get seconds since beat.").with_traceback(tb)

	def getSecondsToNthBeat(self, n):
		if n < len(self.beat_list):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for i in range(self.retry_attempts):
				for beatIndex in range(len(self.beat_list) - (1 + n), 0, -1):
					if time_seconds > self.beat_list[beatIndex]['start']:
						return self.beat_list[beatIndex + n]['start'] - time_seconds
				self.timeoutSleep(i)
				self.reSync()
			self.hardReSync()
			tb = sys.exc_info()[2]
			raise Exception("Could not get seconds to nth beat.").with_traceback(tb)
		print("not enough beats to calculate nth")
		return n

	def getTatum(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			if millis > self.getSongLengthMillis() / 2:
				for tatumIndex in range(len(self.tatum_list) - 2, 0, -1):
					if time_seconds > self.tatum_list[tatumIndex]['start']:
						return tatumIndex
			else:
				for tatumIndex in range(0, len(self.tatum_list) - 2):
					if time_seconds < self.tatum_list[tatumIndex]['start']:
						return tatumIndex - 1
			self.timeoutSleep(i)
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get tatum.").with_traceback(tb)

	def getSecondsToNextTatum(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for tatumIndex in range(len(self.tatum_list) - 2, 0, -1):
				if time_seconds > self.tatum_list[tatumIndex]['start']:
					return self.tatum_list[tatumIndex + 1]['start'] - time_seconds
			self.timeoutSleep(i)
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get seconds to next tatum.").with_traceback(tb)

	def getSecondsSinceTatum(self):
		for i in range(self.retry_attempts):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for tatumIndex in range(len(self.tatum_list) - 2, 0, -1):
				if time_seconds > self.tatum_list[tatumIndex]['start']:
					return time_seconds - self.tatum_list[tatumIndex]['start']
			self.timeoutSleep(i)
			self.reSync()
		self.hardReSync()
		tb = sys.exc_info()[2]
		raise Exception("Could not get seconds since tatum.").with_traceback(tb)

	def getSecondsToNthTatum(self, n):
		if n < len(self.tatum_list):
			millis = self.getPosInSongMillis()
			time_seconds = millis / 1000
			for i in range(self.retry_attempts):
				for tatumIndex in range(len(self.tatum_list) - (1 + n), 0, -1):
					if time_seconds > self.tatum_list[tatumIndex]['start']:
						return self.tatum_list[tatumIndex + n]['start'] - time_seconds
				self.timeoutSleep(i)
				self.reSync()
			self.hardReSync()
			tb = sys.exc_info()[2]
			raise Exception("Could not get seconds to nth tatum.").with_traceback(tb)
		print("not enough tatums to calculate nth")
		return 0.1

	def timeoutSleep(self, iteration):
		for i in range(floor(self.retry_wait_time_millis * (1.2 * iteration))):
			time.sleep(0.001)
		return
