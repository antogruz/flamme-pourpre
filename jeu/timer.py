#!/usr/bin/env python3
from unittests import *
from positions import headToTail

# Cette classe gère les temps des coureurs. On lui déclare les arrivées à chaque tour, et en fonction des positions des coureurs, elle met à jour leur temps général
# Cette classe est amenée à changer si les règles du chrono changent.

class Timer:
    def __init__(self):
        self.turnsAfterFirst = 0
        self.best = None

    def arrive(self, riders):
        if not riders:
            return

        if not self.best:
            self.best = headToTail(riders)[0]

        for r in riders:
            timeDelta = 60 * self.turnsAfterFirst
            timeDelta += secondsEarned(self.best)
            timeDelta -= secondsEarned(r)
            r.addTime(timeDelta)

        self.turnsAfterFirst += 1

def secondsEarned(rider):
    return 10 * rider.position()[0]

class TimeTest:
    def __before__(self):
        self.timer = Timer()

    def testOneArrival(self):
        rider = createRider()
        self.timer.arrive([rider])
        assert_equals(0, rider.persistent.time)

    def testTwoArrivals(self):
        first, second = createRider(), createRider()
        self.timer.arrive([first])
        self.timer.arrive([second])
        assert_equals(60, second.persistent.time)

    def testNoArrival(self):
        rider = createRider()
        self.timer.arrive([])
        self.timer.arrive([rider])
        assert_equals(0, rider.persistent.time)

    def testTwoInSameTurn(self):
        first = createRider(3)
        second = createRider(1)
        self.timer.arrive([first, second])
        assert_equals(20, second.persistent.time)

    def testSecondRace(self):
        first = createRider(60)
        first.persistent.time = 90
        second = createRider(62)
        second.persistent.time = 0
        self.timer.arrive([first])
        self.timer.arrive([second])
        assert_equals(90, first.persistent.time)
        assert_equals(40, second.persistent.time)

from riderInRace import RiderInRace
from riderBuilder import RiderBuilder

def createRider(square = 0):
    rb = RiderBuilder()
    return RiderInRace(rb.getResult(), square, 0)


if __name__ == "__main__":
    runTests(TimeTest())

