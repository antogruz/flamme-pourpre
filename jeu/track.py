#!/usr/bin/env python3

class Track():
    def __init__(self, trackDetail):
        self.squares = []
        for section in trackDetail:
            try:
                (count, type, lanes) = section
            except:
                (count, type) = section
                lanes = 2
            for i in range(count):
                self.squares.append((type, lanes))

    def getRoadType(self, square):
        if square >= len(self.squares):
            return "out"
        return self.squares[square][0]

    def getLaneCount(self, square):
        if square >= len(self.squares):
            return 0
        return self.squares[square][1]

    def lastSquare(self):
        return len(self.squares) - 1

    def previousPosition(self, square, lane):
        if lane < self.getLaneCount(square) - 1:
            return (square, lane + 1)
        return (square - 1, 0)


def streamable(road):
    return not road in ["end", "ascent"]

from unittests import runTests, assert_equals

def tests():
    runTests(TrackTest())

class TrackTest():
    def testEmpty(self):
        track = Track([])
        assert_equals("out", track.getRoadType(0))
        assert_equals(0, track.getLaneCount(0))

    def testNormal(self):
        track = Track([(3, "normal", 1)])
        assert_equals("normal", track.getRoadType(1))
        assert_equals(1, track.getLaneCount(1))

if __name__ == "__main__":
    tests()

