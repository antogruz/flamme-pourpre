#!/usr/bin/env python3

from unittests import Tester, assert_equals

def tests():
    RiderTest().runTests()

class RiderTest(Tester):
    def __init__(self):
        self.rider = Rider(0, 0)
        self.race = Race()

    def testRiderAtStart(self):
        assert_equals((0, 0), self.rider.position())

    def testRiderMove(self):
        self.rider.move(1, Race())
        assert_equals((1, 0), self.rider.position())

    def testTwoRiders(self):
        self.race.addRider(1, 0)
        self.rider.move(1, self.race)
        assert_equals((1, 1), self.rider.position())

    def testBlocked(self):
        self.race.addRider(1, 0)
        self.race.addRider(1, 1)
        self.rider.move(1, self.race)
        assert_equals((0, 0), self.rider.position())


class Rider():
    def __init__(self, square, lane):
        self.square = square
        self.lane = lane

    def position(self):
        return (self.square, self.lane)

    def move(self, n, race):
        slot = (self.square + n, 0)
        while not race.free(slot):
            slot = previous(slot)
        self.square, self.lane = slot


def previous(slot):
    if slot[1] == 0:
        return (slot[0], 1)
    return (slot[0] - 1, 0)


class Race():
    def __init__(self):
        self.obstacles = []

    def addRider(self, square, lane):
        self.obstacles.append((square, lane))

    def free(self, slot):
        return not slot in self.obstacles

tests()
