import time
class NowPlaying:
    def __init__(self, sp):
        self.sp = sp
        self.syncSongData()

    def syncSongData(self):
        self.results = self.sp.current_user_playing_track()
        self.progress_ms = self.results['progress_ms']
        self.msStart = time.time()
        
        self.name = self.results['item']['name']
        self.uri = self.results['item']['uri']
        self.songLength = self.results['item']['duration_ms']
        self.isPlaying = self.results['is_playing']
        
        self.analysis = self.sp.audio_analysis(self.uri)
        self.sectionlist = self.analysis['sections']
        self.beatlist = self.analysis['beats']
        self.tatumlist = self.analysis['tatums']
        
        self.features = self.sp.audio_features(self.uri)
        self.tempo = self.features[0]['tempo']

    def reSync(self):
        tempResults = self.sp.current_user_playing_track()
        if self.uri != tempResults['item']['uri']:
            self.syncSongData()
            return()
        self.progress_ms = tempResults['progress_ms']
        self.msStart = time.time()
        self.isPlaying = tempResults['is_playing']

    def getSectionlist(self):
        return self.sectionlist
    
    def getBeatlist(self):
        return self.beatlist

    def getTatumlist(self):
        return self.tatumlist

    def getPosInSongMillis(self):
        deltaMS = (time.time() - self.msStart) * 1000
        return deltaMS + self.progress_ms

    def getSongName(self):
        return self.name

    def getTempo(self):
        return self.tempo

    def getSongLengthMillis(self):
        return self.songLength

    def getIsPlaying(self):
        return self.isPlaying

