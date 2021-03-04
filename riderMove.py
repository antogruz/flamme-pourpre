#!/usr/bin/env python3

from unittests import Tester, assert_equals

def tests():
    RiderTest().runTests()

class RiderTest(Tester):
    def __init__(self):
        self.rider = Rider(0, 0)

    def testRiderAtStart(self):
        assert_equals((0, 0), self.rider.position())

    def testRiderMove(self):
        self.rider.move(1, Race())
        assert_equals((1, 0), self.rider.position())

    def testTwoRiders(self):
        race = Race()
        race.addRider(1, 0)
        self.rider.move(1, race)
        assert_equals((1, 1), self.rider.position())



class Rider():
    def __init__(self, square, lane):
        self.square = square
        self.lane = lane

    def position(self):
        return (self.square, self.lane)

    def move(self, n, race):
        self.square += n
        if not race.free(self.square, 0):
            self.lane = 1

class Race():
    def __init__(self):
        self.obstacles = []

    def addRider(self, square, lane):
        self.obstacles.append((square, lane))

    def free(self, square, lane):
        return not (square, lane) in self.obstacles

tests()
