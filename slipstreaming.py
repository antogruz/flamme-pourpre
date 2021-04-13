#!/usr/bin/env python3

from unittests import assert_equals, Tester
from riderMove import Rider
from track import Track

def tests():
    SlipstremingTester().runTests()

class SlipstremingTester(Tester):
    def __init__(self):
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


def slipstreamingNormal(riders):
    slipstreaming(riders, Track("normal"))

def slipstreaming(riders, track):
    candidates = sorted(riders, key=square)
    while candidates:
        group = getBackTrackGroup(candidates)
        groupIsStreamed = False
        if someCanSlipstream(group, riders, track):
            groupIsStreamed = group.getSlipstream(track)

        if not groupIsStreamed:
            candidates = candidates[len(group.riders):]

def square(rider):
    return rider.position()[0]

def getBackTrackGroup(orderedRiders):
    group = Group()
    group.append(orderedRiders[0])
    for rider in orderedRiders[1:]:
        if partOf(rider, group):
            group.append(rider)
    orderedRider = orderedRiders[len(group.riders):]
    return group

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
        self.riders = sorted(self.riders, key=square, reverse=True)
        groupIsStreamed = False
        for rider in self.riders:
            if not rider.getSlipstream(track):
                return groupIsStreamed
            groupIsStreamed = True

        return groupIsStreamed


def someCanSlipstream(group, allRiders, track):
    for rider in allRiders:
        if canSlipstream(group.head, rider, track):
            return True
    return False

def canSlipstream(square, rider, track):
    if track.getRoadType(rider.square) == "ascent":
        return False

    return rider.square == square + 2

def display(groups):
    for g in groups:
        print("group")
        for rider in g.riders:
            print (rider.position())

if __name__ == "__main__":
    tests()
