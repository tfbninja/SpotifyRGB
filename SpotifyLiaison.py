from credentials import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import sys
from math import *
import serial
import json
from colour import Color
import NowPlaying


def getTimeToNextBeat(millis, beatlist):
    time = millis / 1000
    for beatIndice in range(len(beatlist) - 1, 0, -1):
        if time > beatlist[beatIndice]['start']:
            return beatlist[beatIndice + 1]['start'] - time
    return None
def getTimeSinceBeat(millis, beatlist):
    time = millis / 1000
    for beatIndice in range(len(beatlist) - 1, 0, -1):
        if time > beatlist[beatIndice]['start']:
            return time - beatlist[beatIndice - 1]['start']
    return None
def printDelta(start, message):
    print(str(time.time() - start) + "   " + message)
    

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=id,
                                               client_secret=secret,
                                               redirect_uri="https://example.com/callback",
                                               scope="user-read-currently-playing"))

results = sp.current_user_playing_track()

progress_ms = results['progress_ms']
msStart = time.time()
print("progress in ms: " + str(progress_ms))

uri = results['item']['uri']
print("uri: " + str(results["item"]["uri"]))

"""
for i in results:
    print(str(i) + ": " + str(results[i]))
"""

print("is playing: " + str(results['is_playing']) + "\n\n\n")

start = time.time()
analysis = sp.audio_analysis(uri)
delta = time.time() - start

print("analysis retrieved in %.2f seconds" % (delta,))
"""
for i in analysis:
    print(str(i) + str(analysis[i]))
"""

currentSong = NowPlaying.NowPlaying(sp)
delta = time.time() - msStart
last = 0

ser = serial.Serial('COM3', 74880)

c = Color("blue")

loopIndice = 0
while(True):
    loopIndice += 1
    #delta = time.time() - msStart
    #currentMS = progress_ms + delta * 1000

    if c.hue < 0.998:
        c.hue = c.hue + 0.001
    else:
        c.hue = 0

    successful = False
    while not successful:
        try:
            nextBeat = getTimeToNextBeat(currentSong.getPosInSongMillis(), currentSong.getBeatlist())
            successful = True
        except IndexError:
            currentSong.reSync()

    lastBeat = getTimeSinceBeat(currentSong.getPosInSongMillis(), currentSong.getBeatlist())

    ratio =  (nextBeat ** 2) / (nextBeat + lastBeat ** 2)

    c.luminance = ratio + 0.05

    out = '(' + str(floor(c.red * 255)) + ',' + str(floor(c.green * 255)) + ',' + str(floor(c.blue * 255)) + ')'

    print("name: " + currentSong.getSongName() + "  is playing: " + str(currentSong.getIsPlaying()) + "   " + out + "   " + str(loopIndice))

    ser.write(bytes(out, 'utf-8'))

    if loopIndice % 150 == 0:
        ser.flushInput()
        ser.flushOutput()
    if (loopIndice % 2000 == 0):
        currentSong.reSync()
        loopIndice = 0
    
    #time.sleep(0.001)    
