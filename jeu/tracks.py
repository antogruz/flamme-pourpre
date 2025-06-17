#!/usr/bin/env python3
from track import Track

# Cette classe permet de créer des courses en utilisant la correspondance Lettres/tuiles

def corsoPaseo():
    return createTrack("abcdefghijklmnopqrstu")

def colDuBallon():
    return createTrack("AnLHgceqtrMBoipjDFkSu")

def hauteMontagne():
    return createTrack("abcfimetKGLHJsdopRQNU")

def classicissima():
    return createTrack("AebQRNHPcgikDFsLojmtu")

def rondeVanWevelgem():
    return createTrack("abcmgfteqonLPjkIDHrSu")

def firenzeMilano():
    return createTrack("abcgiDHqntmKOLrepJsfu")


import random
def randomPresetTrack():
    return random.choice([corsoPaseo, colDuBallon, hauteMontagne, classicissima, rondeVanWevelgem, firenzeMilano])()


def createTrack(letters):
    pieces = getPieces()
    roads = []
    for l in split(letters):
        roads += getRoad(pieces[l])
    return Track(roads)

def split(s):
    result = []
    i = 0
    while i < len(s):
        if s[i] == "_":
            result.append(s[i:i+2])
            i += 2
        else:
            result.append(s[i])
            i += 1
    return result

def getPieces():
    d = {}
    d['a'] = "5s21n2"
    for l in "bcdflmn":
        d[l] = "6n2"
    for l in "eghijkopqrst":
        d[l] = "2n2"
    d['u'] = "1n25e2"
    d['A'] = "4s22n2"
    d['B'] = "4d22n2"
    d['C'] = "3n23a2"
    d['D'] = "5a21d2"
    d['F'] = "3d23n2"
    d['L'] = "3a23d2"
    d['M'] = "2n24a2"
    d['N'] = "6a2"
    d['U'] = "2a24e2"
    for l in "EGKOQR":
        d[l] = "2a2"
    for l in "IJST":
        d[l] = "2n2"
    for l in "HP":
        d[l] = "2d2"
    d['4'] = "5r31n2"
    d['_4'] = "1p11p22p12n2"
    return d

def getRoad(s):
    return [decodeTriplet(triplet) for triplet in divide(s)]

def decodeTriplet(triplet):
    return (int(triplet[0]), getLand(triplet[1]), int(triplet[2]))

def getLand(l):
    if l == 'n':
        return "normal"
    if l == 'a':
        return "ascent"
    if l == 's':
        return "start"
    if l == 'd':
        return "descent"
    if l == 'e':
        return "end"
    if l == 'p':
        return "stone"
    if l == 'r':
        return "refuel"

def divide(s):
    return [s[i:i+3] for i in range(0, len(s), 3)]

from unittests import assert_equals, runTests

class TrackCreationTest():
    def testSimpleTrack(self):
        track = createTrack("aC")
        assert_equals("start", track.getRoadType(4))
        assert_equals("normal", track.getRoadType(5))
        assert_equals("normal", track.getRoadType(6))
        assert_equals("ascent", track.getRoadType(10))
        assert_equals(2, track.getLanes(10))

    def testMultiLanes(self):
        track = createTrack("4")
        assert_equals(3, track.getLanes(0))
        assert_equals(2, track.getLanes(5))
        assert_equals("refuel", track.getRoadType(1))

    def testBlackNumbers(self):
        track = createTrack("_4")
        assert_equals(1, track.getLanes(0))
        assert_equals("stone", track.getRoadType(0))

if __name__ == "__main__":
    runTests(TrackCreationTest())

