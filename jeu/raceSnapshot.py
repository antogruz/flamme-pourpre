#!/usr/bin/env python3

# Vue figée de la course à un instant donné, partagée entre tous les coureurs.
# Une instance par tour, créée au début (avant tout mouvement) et passée aux règles
# qui ont besoin du contexte de course (BonusRules, EnergyRules contextuelles, etc.).
# Permet aux talents de connaître la situation d'un coureur (groupes, peloton de tête)
# sans coupler les talents à la classe Race.

from groups import computeGroups


class RaceSnapshot:
    def __init__(self, allRiders):
        self.allRiders = allRiders

    def getGroups(self):
        return computeGroups(self.allRiders)

    def leadingGroup(self):
        return self.getGroups()[-1]

from unittests import assert_equals, runTests
from riderInRace import RiderInRace
from riderBuilder import RiderBuilder

class RaceSnapshotTest:
    def testGetGroupsReturnsAllGroupsTailToHead(self):
        head = createRider(5)
        mid = createRider(2)
        tail = createRider(0)
        snapshot = RaceSnapshot([head, mid, tail])
        groups = snapshot.getGroups()
        assert_equals(3, len(groups))
        assert_equals(0, groups[0].head)
        assert_equals(5, groups[2].head)

    def testLeadingGroupIsTheLastGroup(self):
        head = createRider(5)
        tail = createRider(0)
        snapshot = RaceSnapshot([head, tail])
        assert_equals([head], snapshot.leadingGroup().riders)


def createRider(square):
    rb = RiderBuilder()
    return RiderInRace(rb.getResult(), square, 0)


if __name__ == "__main__":
    runTests(RaceSnapshotTest())
