import random
import time
from math import *

import serial.tools.list_ports
import spotipy
from colour import Color
from spotipy.oauth2 import SpotifyOAuth

import NowPlaying
from credentials import *
from patterns2 import patternManager
import RemoteManager


def printDelta(start, message):
    print(str(time.time() - start) + "   " + message)


# in my highly uneducated opinion, this tends to generate colors that are highly saturated in the red, green,
# or blue direction. This is because one of the r,g,or b is likely to be high, and the others are likely to be lower
def randomishColor():
    total = random.randint(0, 255 * 3)
    random1 = random.randint(0, min(255, total))
    random2 = random.randint(0, min(255, total - random1))
    random3 = random.randint(0, min(255, total - (random1 + random2)))
    randoms = [float(random1), float(random2), float(random3)]
    random.shuffle(randoms)
    outColor = Color(rgb=(randoms[0] / 256, randoms[1] / 256, randoms[2] / 256))
    return outColor


def randomishColorSeed():
    random_obj = random.random()
    total = random_obj.randint(0, 255 * 3)
    random1 = random_obj.randint(0, min(255, total))
    random2 = random_obj.randint(0, min(255, total - random1))
    random3 = random_obj.randint(0, min(255, total - (random1 + random2)))
    randoms = [float(random1), float(random2), float(random3)]
    random_obj.shuffle(randoms)
    out_color = Color(rgb=(randoms[0] / 256, randoms[1] / 256, randoms[2] / 256))
    return out_color


def flushSerialBuffers():
    print("Flushing serial buffers")
    ser.flushInput()
    ser.flushOutput()


def getLoopLength():
    return loopLength


def printStatusToUser(currentSong, patternManagerObj):
    print("Now playing: " + currentSong.getName())
    print("The current pattern is " + str(patternManagerObj.getPatternName()))
    print("next section is in " + str(currentSong.getSecondsToNextSection())[:5] + "s")

    time_signature = currentSong.getTimeSignature()
    print("Time signature: " + str(time_signature))


def nextRandomPattern(currentSong, patternManagerObj):
    patternManagerObj.nextRandomPattern()
    printStatusToUser(currentSong, patternManagerObj)


def nextPattern(patternManagerObj, pattern_name):
    if patternManagerObj.nextPattern(pattern_name):
        printStatusToUser(current_song, patternManagerObj)


def reSync(currentSong, lastSyncTime, syncPeriod):
    if time.time() - lastSyncTime > syncPeriod:
        currentSong.reSync()
        return time.time()
    return lastSyncTime


def hardReSync(currentSong):
    # if loopIndex - hardSyncPeriod > lastHardSyncIndex:
    print("Going to hard re-sync")
    currentSong.hardReSync()
    # return lastHardSyncIndex


sync_period = 10  # seconds
hard_sync_period = sync_period * 1.5
last_sync_time = time.time()
last_hard_sync_time = time.time()
strobes_per_song = 2
strobes_done = 0
current_pattern = 8

loopLength = 0.001

# Spotify variable, manages all API requests
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=id, client_secret=secret, redirect_uri="https://example.com/callback",
                              scope="user-read-currently-playing"))
# The currentSong object stores all the cached data about the song, including the beat list, time signature,
# danceability, and so forth
current_song = NowPlaying.NowPlaying(sp)
# add patterns from patterns folder somehow idk
pattern_list = []  # FIXME (maybe)
pattern_manager = patternManager.patternManager(current_song, pattern_list, current_pattern, strobes_per_song,
                                                strobes_done)  #
printStatusToUser(current_song, pattern_manager)

# This is an integer describing the section in the song that we last knew we were in, if the CURRENT section changes,
# we know to change the pattern
lastSection = current_song.getSection()
lastURI = current_song.getURI()

# This gets a list of all (i think) devices
devices = [port.device for port in serial.tools.list_ports.comports()]
# this makes a list of the respective ports for each device, but only if they're the ones valid for me (you might
# have to change these if you use a different Arduino than I do)
ports = [port for port in devices if port in ['/dev/ttyACM0', '/dev/ttyUSB0', 'COM3']]
if len(ports) != 1:
    raise Exception('cannot identify port to use')
# Uses the first available serial device
port = ports[0]
ser = serial.Serial(port, 57600)
flushSerialBuffers()
rm = RemoteManager.RemoteManager(ser)

# c is the variable we're using to store the color we're going to send over Serial to the Arduino
c = Color("Blue")

# This is the index for the loop that we are in, when the song changes it resets to 0
loop_index = 0

# This is the main loop, where all the pattern algorithms are run
while True:

    # We time the loop length, necessary for at least one pattern
    loopStart = time.time()

    if current_song.isPlaying():

        # This checks if we're near the end of the song, 3000ms is my crossfade
        if current_song.getPosInSongMillis() >= current_song.getSongLengthMillis() - 3500:
            pattern_manager.processSongChange()
            nextPattern(pattern_manager, 'basic_hue_change')
            while current_song.getURI() == lastURI:
                hardReSync(current_song)
            print(
                "Song change detected in main loop, pos: " + str(current_song.getPosInSongMillis()) + " out of: " + str(
                    current_song.getSongLengthMillis()))
            last_sync_time = last_hard_sync_time = loopStart = time.time()
            lastURI = current_song.getURI()
            lastSection = 0
            loop_index = 1
            strobes_done = 0
            nextRandomPattern(current_song, pattern_manager)
            printStatusToUser(current_song, pattern_manager)

            '''# This checks if we are in the first 5000 milliseconds of the song, because we've still got to query 
            Spotify # for all the info, so we'll just do a simple color change for the time being elif 
            current_song.getPosInSongMillis() < 5000: pattern_manager.nextPattern('basic_hue_change') 
            printStatusToUser() '''
        elif pattern_manager.getPatternName() == 'basic_hue_change':
            nextRandomPattern(current_song, pattern_manager)
        else:
            # if we JUST changed sections, we want to update a few things
            this_section = current_song.getSection()
            if this_section != lastSection:
                lastSection = this_section
                nextRandomPattern(current_song, pattern_manager)
                printStatusToUser(current_song, pattern_manager)
    else:
        nextPattern(pattern_manager, 'basic_hue_change')
        print("not playing")
        pass

    pattern_manager.iteratePatternColor()
    c = pattern_manager.getPatternColor()
    convertedRGB = [max(min(floor(c.red * 255), 255), 0), max(min(floor(c.green * 255), 255), 0),
                    max(min(floor(c.blue * 255), 255), 0)]

    out = '(' + str(convertedRGB[0]) + ',' + str(convertedRGB[1]) + ',' + str(convertedRGB[2]) + ')'

    time.sleep(0.005)  # give serial a breather

    ser.write(bytes(out, 'utf-8'))  # tell the arduino what color to display. format: '(RED,GREEN,BLUE)', where RED,
    # GREEN, and BLUE are integers between 0 and 255

    if loop_index % 2500 == 0:
        # the serial would bug out after a while if i didn't do this regularly
        flushSerialBuffers()

    # make sure we're still doing lights to the right song/beat
    last_sync_time = reSync(current_song, last_sync_time, sync_period)

    loop_index += 1
    loopLength = (time.time() - loopStart) * 1000
