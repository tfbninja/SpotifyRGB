from credentials import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import sys
from math import *
import serial.tools.list_ports
import serial
import json
from colour import Color
import NowPlaying

def getTimeToNextSection(millis, sectionlist):
    time = millis / 1000
    for sectionIndice in range(len(sectionlist) - 1, 0, -1):
        if time > sectionlist[sectionIndice]['start']:
            return sectionlist[sectionIndice + 1]['start'] - time
    return None
def getTimeSinceSection(millis, sectionlist):
    time = millis / 1000
    for sectionIndice in range(len(sectionlist) - 1, 0, -1):
        if time > sectionlist[sectionIndice]['start']:
            return time - sectionlist[sectionIndice - 1]['start']
    return None
def getSection(millis, sectionlist):
    time = millis / 1000
    for sectionIndice in range(len(sectionlist) - 1, 0, -1):
        if time > sectionlist[sectionIndice]['start']:
            return sectionIndice
    return None
def getTimeToNextBeat(millis, beatlist):
    time = millis / 1000
    for beatIndice in range(len(beatlist) - 1, 0, -1):
        if time > beatlist[beatIndice]['start']:
            return beatlist[beatIndice + 1]['start'] - time
    return None
def getTimeToNthBeat(millis, beatlist, n):
    time = millis / 1000
    for beatIndice in range(len(beatlist) - 1, 0, -1):
        if time > beatlist[beatIndice]['start']:
            return beatlist[beatIndice + n]['start'] - time
    return None
def getTimeSinceBeat(millis, beatlist):
    time = millis / 1000
    for beatIndice in range(len(beatlist) - 1, 0, -1):
        if time > beatlist[beatIndice]['start']:
            return time - beatlist[beatIndice - 1]['start']
    return None
def getTimeToNextTatum(millis, tatumlist):
    time = millis / 1000
    for tatumIndice in range(len(tatumlist) - 1, 0, -1):
        if time > tatumlist[tatumIndice]['start']:
            return tatumlist[tatumIndice + 1]['start'] - time
    return None
def getTimeSinceTatum(millis, tatumlist):
    time = millis / 1000
    for tatumIndice in range(len(tatumlist) - 1, 0, -1):
        if time > tatumlist[tatumIndice]['start']:
            return time - tatumlist[tatumIndice - 1]['start']
    return None
def printDelta(start, message):
    print(str(time.time() - start) + "   " + message)

patterns = ['color_swirl', 'disco', 'bi-polar']
currentPattern = 2
currentHue = 0
lastSection = 0

polarColors = [Color('Green', hue=0.35833), Color('Blue', hue=(229/360)), Color('#c40ebe'), Color('#c40e3f'), Color('#e3bd12')]

currentPolarColor = polarColors[0]
loopLength = 0.001

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
#analysis = sp.audio_analysis(uri)
delta = time.time() - start

print("analysis retrieved in %.2f seconds" % (delta,))
"""
for i in analysis:
    print(str(i) + str(analysis[i]))
"""

currentSong = NowPlaying.NowPlaying(sp)
delta = time.time() - msStart
last = 0

devices = [port.device for port in serial.tools.list_ports.comports()]
ports = [port for port in devices if port in ['/dev/ttyACM0','/dev/ttyUSB0','COM3']]
if len(ports) != 1:
    raise Exception('cannot identify port to use')
port = ports[0]

ser = serial.Serial(port, 74880)

c = Color("blue")

loopIndice = 0
loopStart = time.time()

while(True):
    loopIndice += 1

    if getSection(currentSong.getPosInSongMillis(), currentSong.getSectionlist()) > lastSection:
        lastSection = getSection(currentSong.getPosInSongMillis(), currentSong.getSectionlist())
        currentPattern += 1
        if currentPattern > len(patterns) - 1:
            currentPattern = 0
        
    if currentPattern == 0:
        if c.hue < 0.998:
            c.hue = c.hue + 0.0005
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
        
        successful = False
        while not successful:
            try:
                ratio =  (nextBeat ** 2) / (nextBeat + lastBeat ** 2)
                successful = True
            except:
                currentSong.reSync()
                break

        c.luminance = ratio + 0.05
    elif currentPattern == 1:
        hues = [Color("Red"), Color("Blue"), Color("White")]
        
        if loopIndice % 200 == 0:
            currentHue += 1
            if currentHue > len(hues) - 1:
                currentHue = 0
        c = hues[currentHue]

        successful = False
        while not successful:
            try:
                nextBeat = getTimeToNextTatum(currentSong.getPosInSongMillis(), currentSong.getTatumlist())
                successful = True
            except IndexError:
                currentSong.reSync()

        if nextBeat < 0.02:
            c.luminance = 1
        else:
            c.luminance = 0.01
    elif currentPattern == 2:
        oneAndAHalfBeatTime = (getTimeToNthBeat(currentSong.getPosInSongMillis(), currentSong.getTatumlist(), 4) - getTimeToNthBeat(currentSong.getPosInSongMillis(), currentSong.getTatumlist(), 1)) / 2 * 1000 # Calculates time of one and a half beats in millis
        ratio = (loopLength * 1000) / oneAndAHalfBeatTime # calculates ratio of one loop time to one and a half beat time, all in millis
        hueSpectrumDistance = 0
        if currentPolarColor.hue > polarColors[0].hue and polarColor.hue < polarColors[1].hue: # we are in green-blue segment
            hueSpectrumDistance = polarColors[1].hue - polarColors[0].hue
        elif currentPolarColor.hue >= polarColors[1].hue and currentPolarColor.hue < polarColors[2].hue or currentPolarColor.hue < polarColors[3].hue and currentPolarColor.hue >= polarColors[2].hue: # we are in purple segment
            hueSpectrumDistance = (polarColors[2].hue - polarColors[1].hue) + (polarColors[3].hue - polarColors[2].hue) # hue dist between green, purple, and red
        elif currentPolarColor.hue > polarColors[3].hue and polarColor.hue < polarColors[4].hue: # we are in red-orange segment
            hueSpectrumDistance = polarColors[3].hue - polarColors[4].hue
        currentPolarColor.hue += ratio * hueSpectrumDistance

    out = '(' + str(floor(c.red * 255)) + ',' + str(floor(c.green * 255)) + ',' + str(floor(c.blue * 255)) + ')'

    print("name: " + currentSong.getSongName() + "  is playing: " + str(currentSong.getIsPlaying()) + "   " + str(currentPattern) + "   " + out + "   " + str(loopIndice))

    ser.write(bytes(out, 'utf-8'))

    if loopIndice % 150 == 0:
        ser.flushInput()
        ser.flushOutput()
    if (loopIndice % 2000 == 0):
        currentSong.reSync()
        loopIndice = 0
    loopLength = time.time() - loopStart / 1000
