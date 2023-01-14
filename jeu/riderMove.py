#!/usr/bin/env python3

from track import streamable

# Cette classe regroupe les méthodes permettant à un coureur de se déplacer sur un circuit.
# Elle est responsable de toutes les règles de déplacement (terrain, aspiration).
# Elle doit être modifiée si les règles de déplacement changent, et les instances doivent être modifiées si un coureur ne suit plus les règles de déplacement de base (aspiré en montagne, avance de 6 en descente, peut dépasser les coureurs, etc.
# TODO La responsabilité de l'aspiration est pour le moment un peu partagée avec slipstream : il serait facile de faire qu'un coureur soit capable d'être aspiré en montagne, mais difficile de le faire être aspiré à 2 cases ou bien qu'il aspire ses co-équipiers de plus loin
# TODO Séparer la responsabilité de donner la position avec celle de connaitre les règles de déplacement. Finalement, ce sont deux choses différentes. Les mouvements du rider peuvent dépendre des règles du jeu spécifiques à chaque coureur. Et pour les mettre en oeuvre, on a besoin d'une entité sur laquelle modifier la position

class Rider():
    def __init__(self, square, lane):
        self.square = square
        self.lane = lane

    def position(self):
        return (self.square, self.lane)

    def getSquare(self):
        return self.square

    def move(self, distance, track, obstacles):
        distance = self.adaptDistanceToRoadType(distance, track)
        self.square, self.lane = self.findAvailableSlot(obstacles, self.square + distance)

    def getSlipstream(self, track):
        if not streamable(track.getRoadType(self.square)):
            return False

        self.square += 1
        return True

    def adaptDistanceToRoadType(self, distance, track):
        starting = track.getRoadType(self.square)
        if starting == "descent":
            distance = max(distance, 5)

        while track.getRoadType(self.square + distance) == "out":
            distance -= 1

        while not ascentValid(track, self.square, distance):
            distance -= 1

        return distance

    def findAvailableSlot(self, obstacles, square):
            slot = (square, 0)
            while not (obstacles.isFree(slot) ) :
                if slot == self.position():
                    return slot
                slot = previous(slot)
            return slot


def ascentValid(race, start, distance):
    return distance <= 5 or not containsAscent(race, start, start + distance)

def containsAscent(race, start, end):
    for i in range(start, end + 1):
        if race.getRoadType(i) == "ascent":
            return True
    return False

def previous(slot):
    if slot[1] == 0:
        return (slot[0], 1)
    return (slot[0] - 1, 0)


from unittests import runTests, assert_equals

class RiderTest():
    def __before__(self):
        self.rider = Rider(0, 0)
        self.race = Race()

    def move(self, distance):
        self.rider.move(distance, self.race, self.race)

    def testRiderAtStart(self):
        assert_equals((0, 0), self.rider.position())

    def testRiderMove(self):
        self.move(1)
        assert_equals((1, 0), self.rider.position())

    def testTwoRiders(self):
        self.race.addRider(1, 0)
        self.move(1)
        assert_equals((1, 1), self.rider.position())

    def testBlocked(self):
        self.race.addRider(1, 0)
        self.race.addRider(1, 1)
        self.move(1)
        assert_equals((0, 0), self.rider.position())

    def testDescent(self):
        self.race.setAll("descent")
        self.move(1)
        assert_equals((5, 0), self.rider.position())

    def testEndOfRace(self):
        self.race = Race(4)
        self.move(4)
        assert_equals((3, 0), self.rider.position())

    def testStartInAscent(self):
        self.race.setAll("ascent")
        self.move(9)
        assert_equals((5, 0), self.rider.position())

    def testThroughAscent(self):
        self.race.set("ascent", 1)
        self.move(9)
        assert_equals((5, 0), self.rider.position())

    def testStopBeforeAscent(self):
        self.race.set("ascent", 7)
        self.move(9)
        assert_equals((6, 0), self.rider.position())

    def testShouldStayAtSamePositionIfBlocked(self):
        self.race.addRider(0, 0) # Myself
        self.race.addRider(1, 0)
        self.race.addRider(1, 1)
        self.move(1)
        assert_equals((0, 0), self.rider.position())


class Race():
    def __init__(self, length = 100):
        self.obstacles = []
        self.length = length
        self.setAll("normal")

    def addRider(self, square, lane):
        self.obstacles.append((square, lane))

    def setAll(self, field):
        self.field = [field for i in range(self.length)]

    def set(self, field, square):
        self.field[square] = field


    def getRoadType(self, square):
        if square >= self.length:
            return "out"
        return self.field[square]

    def isFree(self, slot):
        return not slot in self.obstacles



if __name__ == "__main__":
    runTests(RiderTest())
