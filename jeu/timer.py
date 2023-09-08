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
            r.time += 60 * self.turnsAfterFirst
            r.time += secondsEarned(self.best)
            r.time -= secondsEarned(r)

        self.turnsAfterFirst += 1

def secondsEarned(rider):
    return 10 * rider.position()[0]

class TimeTest:
    def __before__(self):
        self.timer = Timer()

    def testOneArrival(self):
        rider = Rider()
        self.timer.arrive([rider])
        assert_equals(0, rider.time)

    def testTwoArrivals(self):
        first, second = Rider(), Rider()
        self.timer.arrive([first])
        self.timer.arrive([second])
        assert_equals(60, second.time)

    def testNoArrival(self):
        rider = Rider()
        self.timer.arrive([])
        self.timer.arrive([rider])
        assert_equals(0, rider.time)

    def testTwoInSameTurn(self):
        first = Rider(3)
        second = Rider(1)
        self.timer.arrive([first, second])
        assert_equals(20, second.time)

    def testSecondRace(self):
        first = Rider(60)
        first.time = 90
        second = Rider(62)
        second.time = 0
        self.timer.arrive([first])
        self.timer.arrive([second])
        assert_equals(90, first.time)
        assert_equals(40, second.time)


class Rider:
    def __init__(self, square = 0, lane = 0):
        self.square = square
        self.lane = lane
        self.time = 0

    def position(self):
        return (self.square, self.lane)




if __name__ == "__main__":
    runTests(TimeTest())

