#!/usr/bin/env python3

def createTrack():
    detail = [(5, "start"), (8, "normal"), (6, "ascent"), (4, "descent"), (32, "normal"), (5, "end")]
    return Track(detail)

class Track():
    def __init__(self, trackDetail):
        self.squares = []
        for (count, type) in trackDetail:
            for i in range(count):
                self.squares.append(type)

    def getRoadType(self, square):
        if square >= len(self.squares):
            return "out"
        return self.squares[square]

from unittests import Tester, assert_equals

def tests():
    TrackTest().runTests()

class TrackTest(Tester):
    def testEmpty(self):
        track = Track([])
        assert_equals("out", track.getRoadType(0))

    def testNormal(self):
        track = Track([(3, "normal")])
        assert_equals("normal", track.getRoadType(1))

if __name__ == "__main__":
    tests()

