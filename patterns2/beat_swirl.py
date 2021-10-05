from colour import Color

from patterns2.pattern import pattern


# from SpotifyLiaison import getLoopLength

class beat_swirl(pattern):

    @staticmethod
    def isDisco():
        return False

    @staticmethod
    def getName():
        return "beat_swirl"

    def __init__(self, now_playing):
        self.current_song = now_playing
        self.starting_color = Color('#38e84c')
        self.color = self.starting_color
        self.loop_time = 2

    def iterate(self):
        # Calculates time of one and a half beats in millis
        one_and_a_half_beat_time = ((self.current_song.getSecondsToNthBeat(4) -
                                     self.current_song.getSecondsToNthBeat(1)) / 2) * 1000

        # calculates ratio of one loop time to one and a half
        # beat time, all in millis
        # ratio = getLoopLength() / one_and_a_half_beat_time
        ratio = self.loop_time + 0.00001 / one_and_a_half_beat_time + 0.00001

        self.color.hue += min(max(ratio, 0), 0.1)
        if self.color.hue > 1:
            self.color.hue = 0

    def getColor(self):
        return self.color

    def processSongChange(self):
        self.color = self.starting_color
