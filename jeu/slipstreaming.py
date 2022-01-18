#!/usr/bin/env python3

from unittests import assert_equals, runTests
from riderMove import Rider
from track import Track, streamable

def tests():
    runTests(SlipstremingTester())

class SlipstremingTester():
    def __before__(self):
        self.rider = Rider(0, 0)
        self.track = Track([(10, "normal")])
        self.others = []

    def slipstream(self):
        slipstreaming([self.rider] + self.others, self.track)

    def addRider(self, square):
        self.others.append(Rider(square, 0))

    def assertPosition(self, square):
        assert_equals((square, 0), self.rider.position())

    def testOneRiderDontMove(self):
        self.slipstream()
        self.assertPosition(0)

    def testTwoRiders(self):
        self.addRider(2)
        self.slipstream()
        self.assertPosition(1)

    def testTooFar(self):
        self.addRider(3)
        self.slipstream()
        self.assertPosition(0)

    def testNoSlipstreamInSameGroup(self):
        self.addRider(1)
        self.addRider(2)
        self.slipstream()
        self.assertPosition(0)

    def test3Groups(self):
        self.rider = Rider(3, 0)
        self.addRider(0)
        self.addRider(5)
        self.slipstream()
        self.assertPosition(4)

    def testWholeGroupStreamed(self):
        self.rider = Rider(1, 0)
        self.addRider(0)
        self.addRider(2)
        self.addRider(4)
        self.slipstream()
        self.assertPosition(2)

    def testChainStream(self):
        self.addRider(2)
        self.addRider(4)
        self.slipstream()
        self.assertPosition(2)

    def testRiderInAscentIsNotStreamed(self):
        self.track = Track([(1, "ascent"), (10, "normal")])
        self.addRider(2)
        self.slipstream()
        self.assertPosition(0)

    def testRiderInAscentCannotStreamOthers(self):
        self.track = Track([(2, "normal"), (1, "ascent")])
        self.addRider(2)
        self.slipstream()
        self.assertPosition(0)

    def testHeadOfGroupInAscent(self):
        self.track = Track([(1, "normal"), (1, "ascent"), (2, "normal")])
        self.addRider(1)
        self.addRider(3)
        self.slipstream()
        self.assertPosition(0)

    def testBackOfGroupInAscent(self):
        track = Track([(1, "ascent"), (9, "normal")])
        grimpeur = Rider(0, 0)
        rouleur = Rider(1, 0)
        streamer = Rider(3, 0)
        slipstreaming([grimpeur, rouleur, streamer], track)
        assert_equals((0, 0), grimpeur.position())
        assert_equals((2, 0), rouleur.position())

    def testNoSlipstreamingAfterEnd(self):
        self.track = Track([(5, "end")])
        self.addRider(2)
        self.slipstream()
        self.assertPosition(0)

    def testSlipstreamLogs(self):
        self.track = Track([(10, "normal")])
        self.addRider(1)
        self.addRider(3)
        self.addRider(4)
        self.addRider(6)
        riders = [self.rider] + self.others
        logger = Logger()
        slipstreaming(riders, self.track, logger)
        assert_equals([[2, 1], [5, 4, 3, 2]], logger.groups)

class No:
    def logGroup(self, riders):
        pass

class Logger():
    def __init__(self):
        self.groups = []

    def logGroup(self, riders):
        self.groups.append([r.getSquare() for r in riders])



def slipstreaming(riders, track, logger = No()):
    candidates = tailToHead(riders)
    while candidates:
        group, candidates = popBackTrackGroup(candidates)

        if someCanSlipstream(group, candidates, track):
            streamedRiders = group.getSlipstream(track)
            logger.logGroup(headTotail(streamedRiders))
            candidates = tailToHead(streamedRiders) + candidates


def popBackTrackGroup(orderedRiders):
    group = Group()
    group.append(orderedRiders[0])
    for rider in removeFirsts(orderedRiders, 1):
        if partOf(rider, group):
            group.append(rider)

    return group, removeFirsts(orderedRiders, len(group.riders))

def partOf(rider, group):
    return rider.position()[0] <= group.head + 1

class Group():
    def __init__(self):
        self.riders = []
        self.head = -10

    def isEmpty(self):
        return self.riders

    def append(self, rider):
        self.riders.append(rider)
        self.head = rider.position()[0]

    def getSlipstream(self, track):
        self.riders = headTotail(self.riders)
        for i, rider in enumerate(self.riders):
            if not rider.getSlipstream(track):
                return keepFirsts(self.riders, i)

        return self.riders

def tailToHead(riders):
    return sorted(riders, key = square)

def headTotail(riders):
    return sorted(riders, key = square, reverse = True)

def square(rider):
    return rider.position()[0]

def removeFirsts(l, count):
    return l[count:]

def keepFirsts(l, count):
    return l[0:count]

def someCanSlipstream(group, allRiders, track):
    for rider in allRiders:
        if canSlipstream(group.head, rider, track):
            return True
    return False

def canSlipstream(square, rider, track):
    if not streamable(track.getRoadType(rider.getSquare())):
        return False

    return rider.getSquare() == square + 2

def display(groups):
    for g in groups:
        print("group")
        for rider in g.riders:
            print (rider.position())

if __name__ == "__main__":
    tests()
