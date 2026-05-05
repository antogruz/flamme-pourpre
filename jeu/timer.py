#!/usr/bin/env python3
from unittests import *
from positions import headToTail

# Cette classe gère les temps des coureurs. On lui déclare les arrivées à chaque tour, et en fonction des positions des coureurs, elle met à jour leur temps général
# Cette classe est amenée à changer si les règles du chrono changent.

class Timer:
    def __init__(self):
        self.turnsAfterFirst = 0
        self.best = None
        self.raceTimes = {}

    def arrive(self, riders):
        if not riders:
            if self.best:
                self.turnsAfterFirst += 1
            return

        if not self.best:
            self.best = headToTail(riders)[0]

        for r in riders:
            timeDelta = 60 * self.turnsAfterFirst
            timeDelta += secondsEarned(self.best)
            timeDelta -= secondsEarned(r)
            self.raceTimes[r] = timeDelta

        self.turnsAfterFirst += 1

    def getRaceTime(self, rider):
        return self.raceTimes[rider]

def secondsEarned(rider):
    return 10 * rider.position()[0]

class TimeTest:
    def __before__(self):
        self.timer = Timer()

    def testOneArrival(self):
        rider = createRider()
        self.timer.arrive([rider])
        assert_equals(0, self.timer.getRaceTime(rider))

    def testTwoArrivals(self):
        first, second = createRider(), createRider()
        self.timer.arrive([first])
        self.timer.arrive([second])
        assert_equals(60, self.timer.getRaceTime(second))

    def testNoArrival(self):
        rider = createRider()
        self.timer.arrive([])
        self.timer.arrive([rider])
        assert_equals(0, self.timer.getRaceTime(rider))

    def testTwoInSameTurn(self):
        first = createRider(3)
        second = createRider(1)
        self.timer.arrive([first, second])
        assert_equals(20, self.timer.getRaceTime(second))

    def testSeveralTurnsBetweenArrivals(self):
        first, second = createRider(), createRider()
        self.timer.arrive([first])
        self.timer.arrive([])
        self.timer.arrive([second])
        assert_equals(120, self.timer.getRaceTime(second))

from riderInRace import RiderInRace
from riderBuilder import RiderBuilder

def createRider(square = 0):
    rb = RiderBuilder()
    return RiderInRace(rb.getResult(), square, 0)


if __name__ == "__main__":
    runTests(TimeTest())

