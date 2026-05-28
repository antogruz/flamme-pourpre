#!/usr/bin/env python3

from unittests import runTests, assert_equals
# Cette fonction change si les règles de fatigue changent.
# Par exemple si les coureurs en montagne se fatiguent systématiquement, ou bien si un coureur ne fait plus obstactle aux autres et les laisse se fatiguer.
# Pour qu'un type de coureur soit exempté d'une fatigue dans certaines conditions, on attache une ExhaustionRule à son Personnage (cf. Cols en solo).


class ExhaustionRule:
    """Interface pour les règles d'exemption de fatigue d'un coureur.

    Implémenter pour empêcher la fatigue automatique de fin de tour
    lorsqu'une condition est remplie (terrain, allié, état du tour, etc.).
    Chaque règle attachée au Personnage du coureur isolé est consultée :
    si l'une retourne True, la fatigue n'est pas ajoutée et `onExhaustion`
    n'est pas notifié pour ce coureur.
    """
    def exempts(self, rider):
        """Return True to skip exhaustion for `rider` this turn."""
        pass


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

    def testExemptedRider(self):
        rider = Rider(0)
        rider.personnage.exhaustionRules.append(AlwaysExempts())
        observer = RecordingObserver()
        exhaust([rider], [observer])
        assert_equals(0, rider.exhausts)
        assert_equals([], observer.exhausted)


class Rider():
    def __init__(self, square):
        self.square = square
        self.exhausts = 0
        self.personnage = PersonnageStub()

    def exhaust(self):
        self.exhausts += 1

    def getSquare(self):
        return self.square


class PersonnageStub:
    def __init__(self):
        self.exhaustionRules = []


class AlwaysExempts(ExhaustionRule):
    def exempts(self, rider):
        return True


class RecordingObserver:
    def __init__(self):
        self.exhausted = None

    def onExhaustion(self, exhausted):
        self.exhausted = exhausted


def exhaust(riders, observers = []):
    exhausted = []
    for r in riders:
        if not riderAtPosition(r.getSquare() + 1, riders) and not isExempted(r):
            r.exhaust()
            exhausted.append(r)
    for observer in observers:
        observer.onExhaustion(exhausted)

def isExempted(rider):
    for rule in rider.personnage.exhaustionRules:
        if rule.exempts(rider):
            return True
    return False

def riderAtPosition(square, riders):
    for r in riders:
        if r.getSquare() == square:
            return True
    return False

if __name__ == "__main__":
    tests()
