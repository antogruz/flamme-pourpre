#!/usr/bin/env python3

class Rider():
    def __init__(self, square, lane):
        self.square = square
        self.lane = lane

    def position(self):
        return (self.square, self.lane)

    def move(self, distance, race):
        distance = self.adaptDistanceToRoadType(distance, race)
        self.square, self.lane = findAvailableSlot(race, self.square + distance)

    def adaptDistanceToRoadType(self, distance, race):
        starting = race.getRoadType(self.square)
        if starting == "descent":
            distance = max(distance, 5)

        while not ascentValid(race, self.square, distance):
            distance -= 1
        return distance


def ascentValid(race, start, distance):
    return distance <= 5 or not containsAscent(race, start, start + distance)

def containsAscent(race, start, end):
    for i in range(start, end + 1):
        if race.getRoadType(i) == "ascent":
            return True
    return False

def findAvailableSlot(race, square):
        slot = (square, 0)
        while not (race.isFree(slot) and race.getRoadType(slot[0]) != "out") :
            slot = previous(slot)
        return slot

def previous(slot):
    if slot[1] == 0:
        return (slot[0], 1)
    return (slot[0] - 1, 0)

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


from unittests import Tester, assert_equals

def tests():
    RiderTest().runTests()

class RiderTest(Tester):
    def __init__(self):
        self.rider = Rider(0, 0)
        self.race = Race()

    def testRiderAtStart(self):
        assert_equals((0, 0), self.rider.position())

    def testRiderMove(self):
        self.rider.move(1, Race())
        assert_equals((1, 0), self.rider.position())

    def testTwoRiders(self):
        self.race.addRider(1, 0)
        self.rider.move(1, self.race)
        assert_equals((1, 1), self.rider.position())

    def testBlocked(self):
        self.race.addRider(1, 0)
        self.race.addRider(1, 1)
        self.rider.move(1, self.race)
        assert_equals((0, 0), self.rider.position())

    def testDescent(self):
        self.race.setAll("descent")
        self.rider.move(1, self.race)
        assert_equals((5, 0), self.rider.position())

    def testEndOfRace(self):
        self.race = Race(4)
        self.rider.move(4, self.race)
        assert_equals((3, 0), self.rider.position())

    def testStartInAscent(self):
        self.race.setAll("ascent")
        self.rider.move(9, self.race)
        assert_equals((5, 0), self.rider.position())

    def testThroughAscent(self):
        self.race.set("ascent", 1)
        self.rider.move(9, self.race)
        assert_equals((5, 0), self.rider.position())

    def testStopBeforeAscent(self):
        self.race.set("ascent", 7)
        self.rider.move(9, self.race)
        assert_equals((6, 0), self.rider.position())


tests()
