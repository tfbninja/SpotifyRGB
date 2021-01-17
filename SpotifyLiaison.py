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
import random
import NowPlaying

def getTimeToNextSection(millis, sectionlist):
    time = millis / 1000
    for sectionIndice in range(len(sectionlist) - 2, 0, -1):
        if time > sectionlist[sectionIndice]['start']:
            return sectionlist[sectionIndice + 1]['start'] - time
    return None
def getTimeSinceSection(millis, sectionlist):
    time = millis / 1000
    for sectionIndice in range(len(sectionlist) - 2, 0, -1):
        if time > sectionlist[sectionIndice]['start']:
            return time - sectionlist[sectionIndice - 1]['start']
    return None
def getSection(millis, sectionlist):
    time = millis / 1000
    for sectionIndice in range(len(sectionlist) - 2, 0, -1):
        if time > sectionlist[sectionIndice]['start']:
            return sectionIndice
    return None
def getTimeToNextBeat(millis, beatlist):
    time = millis / 1000
    for beatIndice in range(len(beatlist) - 2, 0, -1):
        if time > beatlist[beatIndice]['start']:
            return beatlist[beatIndice + 1]['start'] - time
    return None
def getTimeToNthBeat(millis, beatlist, n):
    time = millis / 1000
    for beatIndice in range(len(beatlist) - 2, 0, -1):
        if time > beatlist[beatIndice]['start']:
            return beatlist[beatIndice + n]['start'] - time
    return None
def getTimeSinceBeat(millis, beatlist):
    time = millis / 1000
    for beatIndice in range(len(beatlist) - 2, 0, -1):
        if time > beatlist[beatIndice]['start']:
            return time - beatlist[beatIndice - 1]['start']
    return None
def getTimeToNextTatum(millis, tatumlist):
    time = millis / 1000
    for tatumIndice in range(len(tatumlist) - 2, 0, -1):
        if time > tatumlist[tatumIndice]['start']:
            return tatumlist[tatumIndice + 1]['start'] - time
    return None
def getTimeSinceTatum(millis, tatumlist):
    time = millis / 1000
    for tatumIndice in range(len(tatumlist) - 2, 0, -1):
        if time > tatumlist[tatumIndice]['start']:
            return time - tatumlist[tatumIndice - 1]['start']
    return None
def refreshRandoms(): # re-does all the random components
    fastRandomDiscoColors = [randomishColor(), randomishColor(), randomishColor(), randomishColor()]
    print("fast random disco colors: " + str(fastRandomDiscoColors))

    randMultiplier = float(random.randint(10, 100)) / 100
    randExponentiator = float(random.randint(10, 100)) / 100
    print("randmult: " + str(randMultiplier) + " randExp: " + str(randExponentiator))
    random.shuffle(patterns)
def printDelta(start, message):
    print(str(time.time() - start) + "   " + message)
def randomishColor(): # in my highly uneducated opinion, this tends to generate colors that are highly saturated in the red, green, or blue direction. This is because one of the r,g,or b is likely to be high, and the others are likely to be lower
    total = random.randint(0, 255*3)
    random1 = random.randint(0, min(255, total))
    random2 = random.randint(0, min(255, total - random1))
    random3 = random.randint(0, min(255, total - (random1 + random2)))
    randoms = [float(random1), float(random2), float(random3)]
    random.shuffle(randoms)
    outColor = Color(rgb=(randoms[0] / 256, randoms[1] / 256, randoms[2] / 256))
    return outColor

syncPeriod = 500
patterns = ['color_swirl', 'disco', 'beat_swirl', 'experiment_no_2', 'rand_color_swirl', 'disco_but_with_different_colors', 'super_fast_disco_and_also_random_colors_because_i_said', 'gentle_pulse']
discoesPerSong = 1
discoesDone = 0
currentPattern = random.choice(patterns)
currentHue = 0
lastSection = 0

exp_no_2_color = Color('#4287f5')
exp_no_2_color_bounds = [Color('#4287f5'), Color('#d935db')]

currentPolarColor = Color('#38e84c')
loopLength = 0.001
refreshRandoms()



sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=id,
                                               client_secret=secret,
                                               redirect_uri="https://example.com/callback",
                                               scope="user-read-currently-playing"))

currentSong = NowPlaying.NowPlaying(sp)
last = 0

devices = [port.device for port in serial.tools.list_ports.comports()]
ports = [port for port in devices if port in ['/dev/ttyACM0','/dev/ttyUSB0','COM3']]
if len(ports) != 1:
    raise Exception('cannot identify port to use')
port = ports[0]

ser = serial.Serial(port, 74880)

c = Color("blue")

loopIndice = 0


while(True):
    loopStart = time.time()
    loopIndice += 1

    if currentSong.getIsPlaying():
        if currentSong.getPosInSongMillis() >= currentSong.getSongLengthMillis() - 5:
            currentSong.reSync()
        successful = False
        try:
            if getSection(currentSong.getPosInSongMillis(), currentSong.getSectionlist()) > lastSection:
                lastSection = getSection(currentSong.getPosInSongMillis(), currentSong.getSectionlist())
                refreshRandoms()
                lastPattern = currentPattern
                canBeDisco = discoesDone < discoesPerSong
                while lastPattern == currentPattern or ("disco" in currentPattern and (not canBeDisco)):
                    currentPattern = random.choice(patterns)
                if "disco" in currentPattern:
                    discoesDone += 1
        except:
            currentSong.reSync()
                
        if currentPattern == 'color_swirl':
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
        elif currentPattern == 'disco':
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
                c.red *= 1
                c.green *= 1
                c.blue *= 1
            else:
                c.red *= 0.01
                c.green *= 0.01
                c.blue *= 0.01
        elif currentPattern == 'beat_swirl': # don't ask me what this pattern calculates, all i know is that the color change is somewhat in time with the beat \_:)_/
            oneAndAHalfBeatTime = (getTimeToNthBeat(currentSong.getPosInSongMillis(), currentSong.getTatumlist(), 4) - getTimeToNthBeat(currentSong.getPosInSongMillis(), currentSong.getTatumlist(), 1)) / 2 * 1000 # Calculates time of one and a half beats in millis
            ratio = (loopLength) / oneAndAHalfBeatTime # calculates ratio of one loop time to one and a half beat time, all in millis
            currentPolarColor.hue += (ratio * 0.5) % 1
            c = currentPolarColor
        elif currentPattern == 'experiment_no_2':
            beatTime = getTimeToNthBeat(currentSong.getPosInSongMillis(), currentSong.getTatumlist(), 2) - getTimeToNthBeat(currentSong.getPosInSongMillis(), currentSong.getTatumlist(), 1) # time between next beat and beat after that
            ratio = (loopLength / (beatTime * 1000))
            if exp_no_2_color.hue >= exp_no_2_color_bounds[1].hue:
                exp_no_2_color.hue -= ratio * (exp_no_2_color_bounds[0].hue - exp_no_2_color_bounds[1].hue)
            else:
                exp_no_2_color.hue += ratio * (exp_no_2_color_bounds[0].hue - exp_no_2_color_bounds[1].hue)
            c = exp_no_2_color
        elif currentPattern == 'rand_color_swirl': # rand color swirl
            if c.hue < 0.998:
                c.hue = c.hue + random.randint(-1, 5) / 10000
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
        elif currentPattern == 'disco_but_with_different_colors': # its like the disco function but not just red white or blue
            discoColorHues = [Color('#4ec7c1'), Color('#8715a3'), Color('#d6a727'), Color('#8a0615')]
            
            if loopIndice % 200 == 0:
                currentHue += 1
                if currentHue > len(discoColorHues) - 1:
                    currentHue = 0
            c = discoColorHues[currentHue]

            successful = False
            while not successful:
                try:
                    nextBeat = getTimeToNextTatum(currentSong.getPosInSongMillis(), currentSong.getTatumlist())
                    successful = True
                except IndexError:
                    currentSong.reSync()

            if nextBeat < 0.02:
                c.red *= 1
                c.green *= 1
                c.blue *= 1
            else:
                c.red *= 0.01
                c.green *= 0.01
                c.blue *= 0.01
        elif currentPattern == 'super_fast_disco_and_also_random_colors_because_i_said': # its like the disco function but not just red white or blue
            hues = [Color('#4ec7c1'), Color('#8715a3'), Color('#d6a727'), Color('#8a0615')]
            
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
                c.red *= 1
                c.green *= 1
                c.blue *= 1
            else:
                c.red *= 0.01
                c.green *= 0.01
                c.blue *= 0.01
        elif currentPattern == 'gentle_pulse':
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
                    ratio = (0.2 * ((nextBeat) / (nextBeat + lastBeat))) ** 0.8
                    successful = True
                except:
                    currentSong.reSync()
                    break

            c.luminance = ratio
                
    else:
        c.hue += 0.0001
        c.saturation = 1

    out = '(' + str(floor(c.red * 255)) + ',' + str(floor(c.green * 255)) + ',' + str(floor(c.blue * 255)) + ')'

    print("name: " + currentSong.getSongName() + "  is playing: " + str(currentSong.getIsPlaying()) + "  pattern:" + str(currentPattern) + "   timeTillSectionChange:" + str(getTimeToNextSection(currentSong.getPosInSongMillis(), currentSong.getSectionlist())) + "   sections:" + str(len(currentSong.getSectionlist())) + "   " + out + "   " + str(loopIndice))

    ser.write(bytes(out, 'utf-8'))

    if loopIndice % 150 == 0:
        ser.flushInput()
        ser.flushOutput()
    if (loopIndice % syncPeriod == 0):
        currentSong.reSync()
        loopIndice = 0
    loopLength = (time.time() - loopStart) * 1000
