#!/usr/bin/env python3

class Rider():
    def __init__(self, square, lane):
        self.square = square
        self.lane = lane

    def position(self):
        return (self.square, self.lane)

    def move(self, distance, track, obstacles):
        distance = self.adaptDistanceToRoadType(distance, track)
        self.square, self.lane = self.findAvailableSlot(obstacles, self.square + distance)

    def getSlipstream(self):
        self.square += 1

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


if __name__ == "__main__":
    tests()
