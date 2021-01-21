import time
import sys
#import Threading #later
#test
class NowPlaying:
    def __init__(self, sp):
        self.sp = sp
        self.retry_attempts = 5
        self.results = self.sp.current_user_playing_track()

        self.isPlaying = self.results['is_playing']
        if self.isPlaying:
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
        tempResults = self.sp.current_user_playing_track()
        self.isPlaying = tempResults['is_playing']
        if self.isPlaying:
            if self.uri != tempResults['item']['uri']:
                self.syncSongData()
                return ()
            self.progress_ms = tempResults['progress_ms']
            self.ms_start = time.time()
            self.isPlaying = tempResults['is_playing']

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

    """
    def getTempo(self):
        return self.tempo
    """

    def getTimeSignature(self):
        return self.time_signature

    def getSongLengthMillis(self):
        return self.song_length

    def isPlaying(self):
        if self.isPlaying: # this is in case it's undefined or whatever
            return self.isPlaying
        else:
            return False

    def roundTo4(num):
        return round(num, 4)

    def getSecondsToNextSection(self):
        millis = self.getPosInSongMillis()
        time_seconds = millis / 1000
        for i in range(self.retry_attempts):
            for sectionIndice in range(len(self.section_list) - 2, 0, -1):
                if time_seconds > self.section_list[sectionIndice]['start']:
                    return self.section_list[sectionIndice + 1]['start'] - time_seconds
            self.reSync()
        tb = sys.exc_info()[2]
        raise Exception("Could not get seconds to next section.").with_traceback(tb)
        return None

    def getSecondsSinceSection(self):
        millis = self.getPosInSongMillis()
        time_seconds = millis / 1000
        for i in range(self.retry_attempts):
            for sectionIndice in range(len(self.section_list) - 2, 0, -1):
                if time_seconds > self.section_list[sectionIndice]['start']:
                    return time_seconds - self.section_list[sectionIndice]['start']
            self.reSync()
        tb = sys.exc_info()[2]
        raise Exception("Could not get seconds since section.").with_traceback(tb)
        return None

    def getSection(self):
        millis = self.getPosInSongMillis()
        time_seconds = millis / 1000
        for i in range(self.retry_attempts):
            for sectionIndice in range(len(self.section_list) - 2, 0, -1):
                if time_seconds > self.section_list[sectionIndice]['start']:
                    return sectionIndice
            self.reSync()
        tb = sys.exc_info()[2]
        raise Exception("Could not get section.").with_traceback(tb)

    def getSecondsToNextBeat(self):
        millis = self.getPosInSongMillis()
        time_seconds = millis / 1000
        for i in range(self.retry_attempts):
            for beatIndice in range(len(self.beat_list) - 2, 0, -1):
                if time_seconds > self.beat_list[beatIndice]['start']:
                    return self.beat_list[beatIndice + 1]['start'] - time_seconds
            self.reSync()
        tb = sys.exc_info()[2]
        raise Exception("Could not get seconds to next beat.").with_traceback(tb)

    def getSecondsToNthBeat(self, n):
        millis = self.getPosInSongMillis()
        time_seconds = millis / 1000
        for i in range(self.retry_attempts):
            for beatIndice in range(len(self.beat_list) - 2, 0, -1):
                if time_seconds > self.beat_list[beatIndice]['start']:
                    return self.beat_list[beatIndice + n]['start'] - time_seconds
            self.reSync()
        tb = sys.exc_info()[2]
        raise Exception("Could not get seconds to nth beat.").with_traceback(tb)

    def getSecondsSinceBeat(self):
        millis = self.getPosInSongMillis()
        time_seconds = millis / 1000
        for i in range(self.retry_attempts):
            for beatIndice in range(len(self.beat_list) - 2, 0, -1):
                if time_seconds > self.beat_list[beatIndice]['start']:
                    return time_seconds - self.beat_list[beatIndice]['start']
            self.reSync()
        tb = sys.exc_info()[2]
        raise Exception("Could not get seconds since beat.").with_traceback(tb)

    def getBeat(self):
        millis = self.getPosInSongMillis()
        time_seconds = millis / 1000
        for i in range(self.retry_attempts):
            if millis > currentSong.getSongLengthMillis() / 2:
                for beatIndice in range(len(self.beatlist) - 2, 0, -1):
                    if time_seconds > self.beatlist[beatIndice]['start']:
                        return beatIndice
            else:
                for beatIndice in range(0, len(self.beatlist) - 2):
                    if time_seconds < self.beatlist[beatIndice]['start']:
                        return beatIndice - 1
            self.reSync()
        tb = sys.exc_info()[2]
        raise Exception("Could not get beat.").with_traceback(tb)

    def getSecondsToNextTatum(self):
        millis = self.getPosInSongMillis()
        time_seconds = millis / 1000
        for i in range(self.retry_attempts):
            for tatumIndice in range(len(self.tatum_list) - 2, 0, -1):
                if time_seconds > self.tatum_list[tatumIndice]['start']:
                    return self.tatum_list[tatumIndice + 1]['start'] - time_seconds
            self.reSync()
        tb = sys.exc_info()[2]
        raise Exception("Could not get seconds to next tatum.").with_traceback(tb)

    def getSecondsToNthTatum(self, n):
        millis = self.getPosInSongMillis()
        time_seconds = millis / 1000
        for i in range(self.retry_attempts):
            for tatumIndice in range(len(self.tatum_list) - 2, 0, -1):
                if time_seconds > self.tatum_list[tatumIndice]['start']:
                    return self.tatum_list[tatumIndice + n]['start'] - time_seconds
            self.reSync()
        tb = sys.exc_info()[2]
        raise Exception("Could not get seconds to nth tatum.").with_traceback(tb)

    def getSecondsSinceTatum(self):
        millis = self.getPosInSongMillis()
        time_seconds = millis / 1000
        for i in range(self.retry_attempts):
            for tatumIndice in range(len(self.tatum_list) - 2, 0, -1):
                if time_seconds > self.tatum_list[tatumIndice]['start']:
                    return time_seconds - self.tatum_list[tatumIndice]['start']
            self.reSync()
        tb = sys.exc_info()[2]
        raise Exception("Could not get seconds since tatum.").with_traceback(tb)

    def getTatum(self):
        millis = self.getPosInSongMillis()
        time_seconds = millis / 1000
        for i in range(self.retry_attempts):
            if millis > self.getSongLengthMillis() / 2:
                for tatumIndice in range(len(self.tatum_list) - 2, 0, -1):
                    if time_seconds > self.tatum_list[tatumIndice]['start']:
                        return tatumIndice
            else:
                for tatumIndice in range(0, len(self.tatum_list) - 2):
                    if time_seconds < self.tatum_list[tatumIndice]['start']:
                        return tatumIndice - 1
            self.reSync()
        tb = sys.exc_info()[2]
        raise Exception("Could not get tatum.").with_traceback(tb)
