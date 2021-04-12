#!/usr/bin/env python3

from unittests import assert_equals
from riderMove import Rider

def tests():
    testOneRiderDontMove()
    testTwoRiders()
    testTooFar()
    testNoSlipstreamInSameGroup()
    test3Groups()
    testWholeGroupStreamed()
    testChainStream()


def testOneRiderDontMove():
    rider = Rider(0, 0)
    track = None
    slipstreaming([rider], track)
    assert_equals((0, 0), rider.position())

def testTwoRiders():
    rider = Rider(0, 0)
    aheadRider = Rider(2, 0)
    slipstreaming([aheadRider, rider], None)
    assert_equals((1, 0), rider.position())

def testTooFar():
    rider = Rider(0, 0)
    aheadRider = Rider(3, 0)
    slipstreaming([aheadRider, rider], None)
    assert_equals((0, 0), rider.position())

def testNoSlipstreamInSameGroup():
    rider = Rider(0, 0)
    slipstreaming([rider, Rider(1, 0), Rider(2, 0)], None)
    assert_equals((0, 0), rider.position())

def test3Groups():
    rider = Rider(3, 0)
    slipstreaming([rider, Rider(0, 0), Rider(5, 0)], None)
    assert_equals((4, 0), rider.position())

def testWholeGroupStreamed():
    rider = Rider(1, 0)
    slipstreaming([rider, Rider(0, 0), Rider(2, 0), Rider(4, 0)], None)
    assert_equals((2, 0), rider.position())

def testChainStream():
    rider = Rider(0, 0)
    slipstreaming([rider, Rider(2, 0), Rider(4, 0)], None)
    assert_equals((2, 0), rider.position())


def slipstreaming(riders, track):
    candidates = sorted(riders, key=square)
    while candidates:
        group = getBackTrackGroup(candidates)
        if someCanSlipstream(group, riders):
            for rider in group.riders:
                rider.getSlipstream()
        else:
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
    return rider.position()[0] <= group.endPosition + 1

class Group():
    def __init__(self):
        self.riders = []
        self.endPosition = -10

    def isEmpty(self):
        return self.riders

    def append(self, rider):
        self.riders.append(rider)
        self.endPosition = rider.position()[0]


def someCanSlipstream(group, allRiders):
    for other in allRiders:
        if other.position()[0] == group.endPosition + 2:
            return True
    return False


def display(groups):
    for g in groups:
        print("group")
        for rider in g.riders:
            print (rider.position())

if __name__ == "__main__":
    tests()
