#!/usr/bin/env python3

# Cette classe et ses fonctions associées définissent la notion de "groupe" de coureurs sur la piste :
# un ensemble de coureurs sur des cases consécutives.
# Elle est consommée par le slipstreaming (qui s'en sert pour déterminer qui peut aspirer qui)
# et par les talents qui veulent connaître la position relative d'un coureur dans le peloton.

from positions import tailToHead


class Group():
    def __init__(self):
        self.riders = []
        self.head = -10

    def isEmpty(self):
        return self.riders

    def append(self, rider):
        self.riders.append(rider)
        self.head = rider.position()[0]


def computeGroups(riders):
    groups = []
    candidates = tailToHead(riders)
    while candidates:
        group, candidates = splitByGroupBehind(candidates)
        groups.append(group)
    return list(reversed(groups))


def splitByGroupBehind(orderedRiders):
    group = Group()
    group.append(orderedRiders[0])
    for rider in firstsRemoved(orderedRiders, 1):
        if partOf(rider, group):
            group.append(rider)

    return group, firstsRemoved(orderedRiders, len(group.riders))


def partOf(rider, group):
    return rider.position()[0] <= group.head + 1


def firstsRemoved(l, count):
    return l[count:]


from unittests import assert_equals, runTests
from riderInRace import RiderInRace

class GroupsTester():
    def testComputeGroupsEmpty(self):
        assert_equals([], computeGroups([]))

    def testComputeGroupsSingleRider(self):
        rider = createRider(3)
        groups = computeGroups([rider])
        assert_equals(1, len(groups))
        assert_equals([rider], groups[0].riders)

    def testComputeGroupsContiguousRidersAreOneGroup(self):
        a = createRider(0)
        b = createRider(1)
        c = createRider(2)
        groups = computeGroups([b, a, c])
        assert_equals(1, len(groups))
        assert_equals(3, len(groups[0].riders))

    def testComputeGroupsSplitsByGap(self):
        head = createRider(5)
        mid = createRider(2)
        tail = createRider(0)
        groups = computeGroups([mid, head, tail])
        assert_equals(3, len(groups))
        assert_equals([head], groups[0].riders)
        assert_equals(2, groups[1].head)
        assert_equals(0, groups[2].head)

    def testComputeGroupsHeadToTailOrder(self):
        head = createRider(4)
        midHead = createRider(3)
        tail = createRider(0)
        groups = computeGroups([tail, midHead, head])
        assert_equals(2, len(groups))
        assert_equals(4, groups[0].head)
        assert_equals(0, groups[1].head)


from riderBuilder import RiderBuilder
def createRider(square):
    rb = RiderBuilder()
    return RiderInRace(rb.getResult(), square, 0)


if __name__ == "__main__":
    runTests(GroupsTester())
