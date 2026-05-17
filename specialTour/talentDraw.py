#!/usr/bin/env python3

# Tirage de `count` talents pour le mode SpecialTour.
# Toujours `count` talents tirés (3 par défaut).
# Equité : l'écart entre le nombre de talents tirés pour chaque candidat éligible
# ne dépasse jamais 1.
# Sont éligibles les personnages au plus bas palier de talents.

import random

from unittests import assert_equals, assert_similars, runTests
from specialTour.profiles.personnagesProfiles import PersonnageProfile

def drawTalents(personnages, count = 3):
    return TalentDraw().drawTalents(personnages, count)

class TalentDraw:
    def __init__(self, shuffle = random.shuffle):
        self.shuffle = shuffle

    def drawTalents(self, personnages, count = 3):
        if not personnages:
            return []
        minTier = min(personnage.profile.getCurrentTier() for personnage in personnages)
        eligiblePersonnages = [personnage for personnage in personnages if personnage.profile.getCurrentTier() == minTier]
        return self.drawTalentsOfEligiblePersonnages(eligiblePersonnages, count)

    def drawTalentsOfEligiblePersonnages(self, personnages, count = 3):
        talentsByPersonnage = { personnage: self.shuffled(personnage.profile.getAccessibleTalents()) for personnage in self.shuffled(personnages) }
        result = []
        while len(result) < count:
            for personnage in talentsByPersonnage.keys():
                if not talentsByPersonnage[personnage]:
                    return result
                result.append((personnage,talentsByPersonnage[personnage].pop(0)))
                if len(result) == count:
                    return result
        return result

    def shuffled(self, list):
        result = list.copy()
        self.shuffle(result)
        return result


class TalentA: pass
class TalentB: pass
class TalentC: pass
class TalentD: pass
class TalentE: pass


def fakePersonnage(tiers):
    p = FakePersonnage()
    p.profile = PersonnageProfile("fake", tiers)
    return p


class FakePersonnage:
    pass


def reverseShuffle(list):
    list.reverse()

class TalentDrawTest:
    def testNoPersonnages(self):
        assert_equals([], TalentDraw().drawTalents([]))

    def testSinglePersonnageGetsThreeDistinctTalents(self):
        a = fakePersonnage([[TalentA, TalentB, TalentC]])
        result = TalentDraw(reverseShuffle).drawTalents([a])
        assert_equals([(a, TalentC), (a, TalentB), (a, TalentA)], result)

    def testSinglePersonnageWithoutEnoughTalents(self):
        a = fakePersonnage([[TalentA]])
        result = TalentDraw(reverseShuffle).drawTalents([a])
        assert_similars([(a, TalentA)], result)

    def testTwoPersonnagesGetTwoAndOne(self):
        a = fakePersonnage([[TalentA, TalentB, TalentC]])
        b = fakePersonnage([[TalentD, TalentE]])
        result = TalentDraw(reverseShuffle).drawTalents([a, b])
        assert_similars([(b, TalentE), (a, TalentC), (b, TalentD)], result)

    def testThreePersonnagesGetOneEach(self):
        a = fakePersonnage([[TalentA]])
        b = fakePersonnage([[TalentB]])
        c = fakePersonnage([[TalentC]])
        result = TalentDraw(reverseShuffle).drawTalents([a, b, c])
        assert_similars([(a, TalentA), (b, TalentB), (c, TalentC)], result)

    def testFourPersonnagesAreSampledToThree(self):
        a = fakePersonnage([[TalentA]])
        b = fakePersonnage([[TalentB]])
        c = fakePersonnage([[TalentC]])
        d = fakePersonnage([[TalentD]])
        result = TalentDraw(reverseShuffle).drawTalents([a, b, c, d])
        assert_similars([(b, TalentB), (c, TalentC), (d, TalentD)], result)


    def testOnlyMinTierPersonnagesAreConsidered(self):
        a = fakePersonnage([[TalentA, TalentB, TalentC]])
        b = fakePersonnage([[TalentD], [TalentE]])
        b.profile.nextTier()
        result = TalentDraw(reverseShuffle).drawTalents([a, b])
        assert_similars([(a, TalentA), (a, TalentB), (a, TalentC)], result)

    def testTalentsArePickedFromCurrentTier(self):
        a = fakePersonnage([[TalentA], [TalentB, TalentC, TalentD]])
        a.profile.nextTier()
        result = TalentDraw(reverseShuffle).drawTalents([a])
        assert_similars([(a, TalentB), (a, TalentC), (a, TalentD)], result)


if __name__ == "__main__":
    runTests(TalentDrawTest())
