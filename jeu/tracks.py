#!/usr/bin/env python3
from track import Track

# Cette classe permet de créer des courses en utilisant la correspondance Lettres/tuiles

def corsoPaseo(_ = None):
    return createTrack("abcdefghijklmnopqrstu")

def colDuBallon(_ = None):
    return createTrack("AnLHgceqtrMBoipjDFkSu")

def hauteMontagne(_ = None):
    return createTrack("abcfimetKGLHJsdopRQNU")

def classicissima(_ = None):
    return createTrack("AebQRNHPcgikDFsLojmtu")

def rondeVanWevelgem(_ = None):
    return createTrack("abcmgfteqonLPjkIDHrSu")

def firenzeMilano(_ = None):
    return createTrack("abcgiDHqntmKOLrepJsfu")

def stage7(playersCount):
    if playersCount <= 4:
        return createTrack("a_23gMRPkeqos4cDHjTniu")
    return createTrack("_123gMRPkeqos4cDHjT_9niu")

def stage8(playersCount):
    if playersCount <= 4:
        return createTrack("a_2h4oIcQDF3prsejLktgu")
    return createTrack("_12h4oIcQDF3prsejLktg_9u")

def stage9(playersCount):
    if playersCount <= 4:
        return createTrack("A_23p5_7okjq4e8_6hgirsTu")
    return createTrack("12_93p5_7okjq4e8_6hgirsTu")

def stage10(playersCount):
    if playersCount <= 4:
        return createTrack("a_2h4Lopc5_6r3gqJksteIU")
    return createTrack("_12h4_9Lopc5_6r3gqJksteIU")

def stage11(playersCount):
    if playersCount <= 4:
        return createTrack("a_28_5qgir_3_4sopthk7_6eJu")
    return createTrack("_128_5qgir9_3_4sopthk7_6eJu")

def stage12(playersCount):
    if playersCount <= 4:
        return createTrack("A_24qMOKRFsd3plnhgeTju")
    return createTrack("124qMOKRFsd3pln_9hgeTju")


def allTracksBuilders():
    return [corsoPaseo, colDuBallon, hauteMontagne, classicissima, rondeVanWevelgem, firenzeMilano, stage7, stage8, stage9, stage10, stage11, stage12]

import random
def randomPresetTrack(playersCount):
    return random.choice(allTracksBuilders())(playersCount)


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
    d['1'] = "4s32n3"
    d['_1'] = "5s31n3"
    d['2'] = "5n31n2"
    d['_2'] = "6n2"
    d['3'] = "5r31n2"
    d['_3'] = "2n22p11p21p1"
    d['4'] = "5r31n2"
    d['_4'] = "1p11p22p12n2"
    d['5'] = "1p11p21p11p22p1"
    d['_5'] = "2p14n2"
    d['6'] = "2p11p23p1"
    d['_6'] = "3p11p21p11n2"
    d['7'] = "2n22p11p21p1"
    d['_7'] = "1p11p21p13n2"
    d['8'] = "3n21p11p21p1"
    d['_8'] = "2p11p22p11n2"
    d['9'] = "2r31n2"
    d['_9'] = "2n31n2"
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
        assert_equals(2, track.getLaneCount(10))

    def testMultiLanes(self):
        track = createTrack("4")
        assert_equals(3, track.getLaneCount(0))
        assert_equals(2, track.getLaneCount(5))
        assert_equals("refuel", track.getRoadType(1))

    def testBlackNumbers(self):
        track = createTrack("_4")
        assert_equals(1, track.getLaneCount(0))
        assert_equals("stone", track.getRoadType(0))

if __name__ == "__main__":
    runTests(TrackCreationTest())

