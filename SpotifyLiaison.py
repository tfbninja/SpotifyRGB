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
def getBeat(currentSong):
    millis = currentSong.getPosInSongMillis()
    beatlist = currentSong.getBeatlist()
    time = millis / 1000
    if (millis > currentSong.getSongLengthMillis() / 2):
        for beatIndice in range(len(beatlist) - 2, 0, -1):
            if time > beatlist[beatIndice]['start']:
                return beatIndice
    else:
        for beatIndice in range(0, len(beatlist) - 2):
            if time < beatlist[beatIndice]['start']:
                return beatIndice - 1
    return None
def getTimeToNextTatum(millis, tatumlist):
    time = millis / 1000
    for tatumIndice in range(len(tatumlist) - 2, 0, -1):
        if time > tatumlist[tatumIndice]['start']:
            return tatumlist[tatumIndice + 1]['start'] - time
    return None
def getTimeToNthTatum(millis, tatumlist, n):
    time = millis / 1000
    for tatumIndice in range(len(tatumlist) - 2, 0, -1):
        if time > tatumlist[tatumIndice]['start']:
            return tatumlist[tatumIndice + n]['start'] - time
    return None
def getTimeSinceTatum(millis, tatumlist):
    time = millis / 1000
    for tatumIndice in range(len(tatumlist) - 2, 0, -1):
        if time > tatumlist[tatumIndice]['start']:
            return time - tatumlist[tatumIndice - 1]['start']
    return None
def getTatum(currentSong):
    millis = currentSong.getPosInSongMillis()
    tatumlist = currentSong.getTatumlist()
    time = millis / 1000
    if (millis > currentSong.getSongLengthMillis() / 2):
        for tatumIndice in range(len(tatumlist) - 2, 0, -1):
            if time > tatumlist[tatumIndice]['start']:
                return tatumIndice
    else:
        for tatumIndice in range(0, len(tatumlist) - 2):
            if time < tatumlist[tatumIndice]['start']:
                return tatumIndice - 1
    return None
def refreshRandoms(): # re-does all the random components
    fastRandomDiscoColors = [randomishColor(), randomishColor(), randomishColor(), randomishColor()]
    print("fast random disco colors: " + str(fastRandomDiscoColors))

    randMultiplier = float(random.randint(10, 100)) / 100
    randExponentiator = float(random.randint(10, 100)) / 100
    print("randmult: " + str(randMultiplier) + " randExp: " + str(randExponentiator))
    #random.shuffle(patterns)
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

refreshRandoms()
trifecta_pulse_color = Color("#44f25b")
syncPeriod = 500
patterns = ['color_swirl', 'disco', 'beat_swirl', 'experiment_no_2', 'rand_color_swirl', 'disco_but_with_different_colors', 'super_fast_disco_and_also_random_colors_because_i_said', 'gentle_pulse', 'trifecta_pulse', '2_color_oscillation']
discoesPerSong = 2
discoesDone = 0
currentPattern = 4

discoBar = 0.043
currentHue = 0
lastDiscoBeat = 0

exp_no_2_color = Color('#4287f5')
exp_no_2_color_bounds = [Color('#4287f5'), Color('#d935db')]
exp_no_2_ratio = 0.5

currentPolarColor = Color('#38e84c')

trifecta_pulse_hue_add = 0.31
trifecta_indice = 0
trifecta_last_tatum_no = 0

oscillation_colors = [Color('#34ebcf'), Color('#d66f1c')]
loopLength = 0.001
#random.shuffle(patterns)




sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=id,
                                               client_secret=secret,
                                               redirect_uri="https://example.com/callback",
                                               scope="user-read-currently-playing"))

currentSong = NowPlaying.NowPlaying(sp)
lastSection = getSection(currentSong.getPosInSongMillis(), currentSong.getSectionlist())
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
        try:
            if currentSong.getPosInSongMillis() >= currentSong.getSongLengthMillis() - 5:
                currentSong.reSync()
            successful = False
            try:
                if getSection(currentSong.getPosInSongMillis(), currentSong.getSectionlist()) > lastSection:
                    discoOnOff = [0,0]
                    lastSection = getSection(currentSong.getPosInSongMillis(), currentSong.getSectionlist())
                    currentPattern += random.randint(1,4)
                    currentPattern = currentPattern % len(patterns)
                    refreshRandoms()
                    canBeDisco = discoesDone < discoesPerSong
                    while ("disco" in patterns[currentPattern] and (not canBeDisco)):
                        currentPattern += 1
                        currentPattern = currentPattern % len(patterns)
                    if "disco" in patterns[currentPattern]:
                        discoesDone += 1
            except:
                currentSong.reSync()
                    
            if patterns[currentPattern] == 'color_swirl':
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

                successful = False
                while not successful:
                    try:
                        lastBeat = getTimeSinceBeat(currentSong.getPosInSongMillis(), currentSong.getBeatlist())
                        successful = True
                    except IndexError:
                        currentSong.reSync()
                
                successful = False
                while not successful:
                    try:
                        ratio =  (nextBeat ** 2) / (((nextBeat + lastBeat) / 2) ** 2)
                        successful = True
                    except:
                        currentSong.reSync()
                        break

                c.luminance = max(min(ratio + 0.05, 1), 0)
            elif patterns[currentPattern] == 'disco':
                hues = [Color("Red"), Color("Blue"), Color("White")]

                if getBeat(currentSong) > lastDiscoBeat:
                    lastDiscoBeat = getBeat(currentSong)
                    currentHue += 1
                    if currentHue > len(hues) - 1:
                        currentHue = 0
                c = hues[currentHue]

                successful = False
                while not successful:
                    try:
                        nextTatum = getTimeToNextTatum(currentSong.getPosInSongMillis(), currentSong.getTatumlist())
                        successful = True
                    except IndexError:
                        currentSong.reSync()

                if nextTatum <= discoBar:
                    c.red *= 1
                    c.green *= 1
                    c.blue *= 1
                else:
                    c.red *= 0.01
                    c.green *= 0.01
                    c.blue *= 0.01
            elif patterns[currentPattern] == 'beat_swirl': # don't ask me what this pattern calculates, all i know is that the color change is somewhat in time with the beat \_:)_/
                oneAndAHalfBeatTime = (getTimeToNthBeat(currentSong.getPosInSongMillis(), currentSong.getTatumlist(), 4) - getTimeToNthBeat(currentSong.getPosInSongMillis(), currentSong.getTatumlist(), 1)) / 2 * 1000 # Calculates time of one and a half beats in millis
                ratio = (loopLength) / oneAndAHalfBeatTime # calculates ratio of one loop time to one and a half beat time, all in millis
                currentPolarColor.hue += (ratio * 0.5) % 1
                c = currentPolarColor
            elif patterns[currentPattern] == 'experiment_no_2':
                successful = False
                while not successful:
                    try:
                        beatTime = getTimeToNthBeat(currentSong.getPosInSongMillis(), currentSong.getTatumlist(), 2) - getTimeToNthBeat(currentSong.getPosInSongMillis(), currentSong.getTatumlist(), 1) # time between next beat and beat after that
                        successful = True
                    except:
                        print("Err on line 256")
                        currentSong.reSync()
                if exp_no_2_color.hue > exp_no_2_color_bounds[1].hue:
                    exp_no_2_ratio = 1 -(loopLength / (beatTime * 1000))
                elif exp_no_2_color.hue < exp_no_2_color_bounds[0].hue:
                    exp_no_2_ratio = (loopLength / (beatTime * 1000))
                
                exp_no_2_color.hue = (exp_no_2_ratio * (exp_no_2_color_bounds[0].hue - exp_no_2_color_bounds[1].hue)) + exp_no_2_color_bounds[0].hue
                c = exp_no_2_color
            elif patterns[currentPattern] == 'rand_color_swirl': # rand color swirl
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
                        
                successful = False
                while not successful:
                    try:
                        lastBeat = getTimeSinceBeat(currentSong.getPosInSongMillis(), currentSong.getBeatlist())
                        successful = True
                    except IndexError:
                        currentSong.reSync()
                
                successful = False
                while not successful:
                    try:
                        ratio =  (nextBeat ** 2) / (nextBeat + lastBeat ** 2)
                        successful = True
                    except:
                        currentSong.reSync()
                        break

                c.luminance = min(ratio + 0.05, 0.7)
            elif patterns[currentPattern] == 'disco_but_with_different_colors': # its like the disco function but not just red white or blue
                discoColorHues = [Color('#4ec7c1'), Color('#8715a3'), Color('#d6a727'), Color('#8a0615')]
                
                if loopIndice % 200 == 0:
                    currentHue += 1
                    if currentHue > len(discoColorHues) - 1:
                        currentHue = 0
                c = discoColorHues[currentHue]

                successful = False
                while not successful:
                    try:
                        nextTatum = getTimeToNextTatum(currentSong.getPosInSongMillis(), currentSong.getTatumlist())
                        successful = True
                    except IndexError:
                        currentSong.reSync()

                if nextTatum <= discoBar:
                    c.red *= 1
                    c.green *= 1
                    c.blue *= 1
                else:
                    c.red *= 0.01
                    c.green *= 0.01
                    c.blue *= 0.01
            elif patterns[currentPattern] == 'super_fast_disco_and_also_random_colors_because_i_said': # its like the disco function but not just red white or blue
                hues = [Color('#4ec7c1'), Color('#8715a3'), Color('#d6a727'), Color('#8a0615')]
                
                if loopIndice % 200 == 0:
                    currentHue += 1
                    if currentHue > len(hues) - 1:
                        currentHue = 0
                c = hues[currentHue]

                successful = False
                while not successful:
                    try:
                        nextTatum = getTimeToNextTatum(currentSong.getPosInSongMillis(), currentSong.getTatumlist())
                        successful = True
                    except IndexError:
                        currentSong.reSync()

                if nextTatum <= discoBar:
                    c.red *= 1
                    c.green *= 1
                    c.blue *= 1
                else:
                    c.red *= 0.01
                    c.green *= 0.01
                    c.blue *= 0.01
            elif patterns[currentPattern] == 'gentle_pulse':
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

                successful = False
                while not successful:
                    try:
                        lastBeat = getTimeSinceBeat(currentSong.getPosInSongMillis(), currentSong.getBeatlist())
                        successful = True
                    except IndexError:
                        currentSong.reSync()

                
                successful = False
                while not successful:
                    try:
                        ratio = (0.2 * ((nextBeat) / (nextBeat + lastBeat))) ** 0.8
                        successful = True
                    except:
                        currentSong.reSync()
                        break

                c.luminance = ratio
            elif patterns[currentPattern] == 'trifecta_pulse':
                if trifecta_indice == 3:
                    trifecta_indice = 0
                    trifecta_pulse_color.hue += trifecta_pulse_hue_add
                    trifecta_pulse_color.hue = trifecta_pulse_color.hue % 1
                c = Color(trifecta_pulse_color)

                successful = False
                while not successful:
                    try:
                        nextTatum = getTimeToNextTatum(currentSong.getPosInSongMillis(), currentSong.getTatumlist())
                        successful = True
                    except IndexError:
                        print(IndexError)
                        currentSong.reSync()
                successful = False
                while not successful:
                    try:
                        lastTatum = getTimeSinceTatum(currentSong.getPosInSongMillis(), currentSong.getTatumlist())
                        successful = True
                    except IndexError:
                        print(IndexError)
                        currentSong.reSync()
                
                ratio =  (nextTatum ** 2) / (nextTatum + lastTatum ** 2)
                if getTatum(currentSong) > trifecta_last_tatum_no:
                    trifecta_last_tatum_no = getTatum(currentSong)
                    trifecta_indice += 1

                c.luminance = ratio + 0.05
            elif patterns[currentPattern] == '2_color_oscillation':
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
                        lum_ratio =  (nextBeat ** 2) / ((nextBeat + lastBeat) ** 2)
                        color_ratio = nextBeat / ((lastBeat + nextBeat) / 2)
                        if color_ratio > 0.5:
                            color_ratio = 1 - ((1 - color_ratio) ** 2)
                        else:
                            color_ratio = color_ratio ** 2
                        successful = True
                    except:
                        currentSong.reSync()
                        break
                """
                c.red = min(oscillation_colors[0].red, oscillation_colors[1].red) + (color_ratio * abs(oscillation_colors[0].red - oscillation_colors[1].red))
                c.green = min(oscillation_colors[0].green, oscillation_colors[1].green) + (color_ratio * abs(oscillation_colors[0].green - oscillation_colors[1].green))
                c.blue = min(oscillation_colors[0].blue, oscillation_colors[1].blue) + (color_ratio * abs(oscillation_colors[0].blue - oscillation_colors[1].blue))
                """
                c.hue = min(oscillation_colors[0].hue, oscillation_colors[1].hue) + (color_ratio * abs(oscillation_colors[0].hue - oscillation_colors[1].hue))
                print(color_ratio,end='')
                c.luminance = max(0, min(lum_ratio + 0.05, 1))
            else:
                print("unknown pattern \"" + str(currentPattern) + "\"")
                
        except IndexError:
            print("ran into index error")
            currentSong.reSync()
        try:
            out = '(' + str(floor(c.red * 255)) + ',' + str(floor(c.green * 255)) + ',' + str(floor(c.blue * 255)) + ')'

            print("name: " + currentSong.getSongName() + "  is playing: " + str(currentSong.getIsPlaying()) + "  pattern:" + str(patterns[currentPattern]) + "   timeTillSectionChange:" + str(getTimeToNextSection(currentSong.getPosInSongMillis(), currentSong.getSectionlist())) + "   discobar:" + str(discoBar) + "   " + out + "   " + str(loopIndice))
        except IndexError:
            print("couldn't print??" + str(IndexError.message))
            currentSong.reSync()
    else:
        c.hue += 0.0001
        print(c)
    try:
        out = '(' + str(floor(c.red * 255)) + ',' + str(floor(c.green * 255)) + ',' + str(floor(c.blue * 255)) + ')'

        #print("name: " + currentSong.getSongName() + "  is playing: " + str(currentSong.getIsPlaying()) + "  pattern:" + str(currentPattern) + "   timeTillSectionChange:" + str(getTimeToNextSection(currentSong.getPosInSongMillis(), currentSong.getSectionlist())) + "   sections:" + str(len(currentSong.getSectionlist())) + "   " + out + "   " + str(loopIndice))
    except:
        #currentSong.reSync()
        pass

    ser.write(bytes(out, 'utf-8'))

    if loopIndice % 150 == 0:
        ser.flushInput()
        ser.flushOutput()
    if (loopIndice % syncPeriod == 0):
        currentSong.reSync()
        loopIndice = 0
    loopLength = (time.time() - loopStart) * 1000
