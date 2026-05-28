#!/usr/bin/env python3

from track import streamable, Track

# Ce module définit comment un coureur se déplace sur un circuit en fonction de
# l'énergie d'une carte, du terrain et des obstacles. L'interface MovementRules
# décrit le contrat consommé par RiderInRace ; StandardMovementRules en fournit
# l'implémentation par défaut (terrain, plafond montagne, etc.). Les talents
# peuvent décorer ou remplacer cette implémentation pour modifier les règles
# (bypass de la montagne, bonus en descente, etc.).


class MovementRules:
    """Interface pour les règles de déplacement d'un coureur.

    Une implémentation calcule, pour une carte d'énergie donnée et un état de
    course (position, terrain, obstacles), la nouvelle position du coureur.
    Les talents peuvent fournir un décorateur ou une implémentation alternative,
    en se reposant éventuellement sur une instance existante.
    """
    def computeNewPosition(self, startingPosition, energy, track, obstacles):
        """Calcule et retourne la nouvelle position `(square, lane)` du coureur."""
        pass

    def findAvailableSlot(self, obstacles, startingPosition, distance, track):
        """Trouve la case libre la plus avancée à `distance` cases de `startingPosition`."""
        pass


class StandardMovementRules(MovementRules):
    def computeNewPosition(self, startingPosition, energy, track, obstacles):
        distance = self.adaptDistanceToRoadType(startingPosition[0], energy, track)
        return self.findAvailableSlot(obstacles, startingPosition, distance, track)

    def adaptDistanceToRoadType(self, square, energy, track):
        distance = int(energy)
        starting = track.getRoadType(square)
        if starting == "descent":
            distance = max(distance, 5)
        if starting == "refuel":
            distance = max(distance, 4)

        while track.getRoadType(square + distance) == "out":
            distance -= 1

        while not ascentValid(track, square, distance):
            distance -= 1

        return distance

    def findAvailableSlot(self, obstacles, startingPosition, distance, track):
            slot = (startingPosition[0] + distance, 0)
            while not (obstacles.isFree(slot) ) :
                if slot == startingPosition:
                    return slot
                slot = track.previousPosition(slot[0], slot[1])
            return slot

def ascentValid(track, start, distance):
    return distance <= 5 or not containsAscent(track, start, start + distance)

def containsAscent(track, start, end):
    for i in range(start, end + 1):
        if track.getRoadType(i) == "ascent":
            return True
    return False


from unittests import runTests, assert_equals

class StandardMovementRulesTest():
    def __before__(self):
        self.race = Race()
        self.position = (0, 0)
        self.movementRules = StandardMovementRules()

    def move(self, energy):
        return self.movementRules.computeNewPosition(self.position, energy, self.race.track, self.race)

    def testRiderMove(self):
        assert_equals((1, 0), self.move(1))

    def testTwoRiders(self):
        self.race.addRider(1, 0)
        assert_equals((1, 1), self.move(1))

    def testBlocked(self):
        self.race.set("normal", 1, 1)
        self.race.addRider(1, 0)
        assert_equals((0, 0), self.move(1))

    def testNotBlocked(self):
        self.race.set("normal", 1, 3)
        self.race.addRider(1, 0)
        self.race.addRider(1, 1)
        assert_equals((1, 2), self.move(1))

    def testDescent(self):
        self.race.setAll("descent")
        assert_equals((5, 0), self.move(1))

    def testEndOfRace(self):
        self.race = Race(4)
        assert_equals((3, 0), self.move(4))

    def testStartInAscent(self):
        self.race.setAll("ascent")
        assert_equals((5, 0), self.move(9))

    def testThroughAscent(self):
        self.race.set("ascent", 1)
        assert_equals((5, 0), self.move(9))

    def testStopBeforeAscent(self):
        self.race.set("ascent", 7)
        assert_equals((6, 0), self.move(9))

    def testShouldStayAtSamePositionIfBlocked(self):
        self.race.addRider(0, 0) # Myself
        self.race.addRider(1, 0)
        self.race.addRider(1, 1)
        assert_equals((0, 0), self.move(1))

    def testRefuel(self):
        self.race.setAll("refuel")
        assert_equals((4, 0), self.move(1))

    def testRefuelWithHigherCard(self):
        self.race.setAll("refuel")
        assert_equals((6, 0), self.move(6))

class Race():
    def __init__(self, length = 100):
        self.obstacles = []
        self.length = length
        self.track = Track([(length, "normal", 2)])

    def addRider(self, square, lane):
        self.obstacles.append((square, lane))

    def setAll(self, field):
        self.track = Track([(self.length, field, 2)])

    def set(self, field, square, lanes = 2):
        self.track.squares[square] = (field, lanes)

    def getRoadType(self, square):
        return self.track.getRoadType(square)

    def isFree(self, slot):
        return not slot in self.obstacles


if __name__ == "__main__":
    runTests(StandardMovementRulesTest())
