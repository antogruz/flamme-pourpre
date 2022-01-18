#!/usr/bin/env python3

from unittests import runTests, assert_equals

def tests():
    runTests(ExhaustTester())

class ExhaustTester():
    def testSolo(self):
        rider = Rider(0)
        exhaust([rider])
        assert_equals(1, rider.exhausts)

    def testGroup(self):
        rider = Rider(0)
        exhaust([rider, Rider(1)])
        assert_equals(0, rider.exhausts)

    def testGroups(self):
        firstA = Rider(5)
        secondA = Rider(4)
        firstB = Rider(1)
        secondB = Rider(0)
        exhaust([firstA, secondA, firstB, secondB])
        assert_equals(0, secondA.exhausts)
        assert_equals(1, firstA.exhausts)
        assert_equals(0, secondB.exhausts)
        assert_equals(1, firstB.exhausts)


class Rider():
    def __init__(self, square):
        self.square = square
        self.exhausts = 0

    def exhaust(self):
        self.exhausts += 1

    def getSquare(self):
        return self.square

class NoLogger():
    def logExhaust(self, r):
        pass

def exhaust(riders, logger = NoLogger()):
    for r in riders:
        if not riderAtPosition(r.getSquare() + 1, riders):
            r.exhaust()
            logger.logExhaust(r)

def riderAtPosition(square, riders):
    for r in riders:
        if r.getSquare() == square:
            return True
    return False

if __name__ == "__main__":
    tests()
