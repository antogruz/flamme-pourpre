#!/usr/bin/env python3

from unittests import Tester, assert_equals, assert_similars
from track import Track
from rider import Rider
from cards import Cards
import riderMove
from animation import Logger

def tests():
    RaceTest().runTests()

class RaceTest(Tester):
    def __init__(self):
        self.track = Track([(5, "normal"), (3, "end")])

    def createRace(self, riders):
        return Race(self.track, riders, [SimplePlayer(copy(riders), 2)], Logger())

    def testCreateRace(self):
        riders = [createRider(0, 0)]
        race = self.createRace(riders)
        assert_equals(False, race.isOver())
        assert_similars([], race.ranking())

    def testRaceOver(self):
        race = self.createRace([])
        assert_equals(True, race.isOver())

    def testRaceIsOverIfAllRidersHavePassedLine(self):
        race = self.createRace([createRider(5, 0)])
        assert_equals(True, race.isOver())

    def testRiderMovesAfterATurn(self):
        rider = createRider(0, 0)
        race = self.createRace([rider])
        race.newTurn()
        assert_equals(2, rider.position()[0])

    def testArrival(self):
        rider = createRider(4, 0)
        race = self.createRace([rider, createRider(0, 0)])
        race.newTurn()
        assert_similars([rider], race.ranking())

    def testDontPlayForArrivedRiders(self):
        rider = createRider(5, 0)
        rider.nextMove = 100
        race = self.createRace([rider])
        race.newTurn()
        assert_equals(100, rider.nextMove)

    def testRanking(self):
        first = createRider(5, 0)
        second = createRider(4, 0)
        third = createRider(3, 0)
        fourth = createRider(0, 0)
        race = self.createRace([fourth, second, third, first])
        while not race.isOver():
            race.newTurn()
        assert_equals([first, second, third, fourth], race.ranking())


def copy(list):
    return [l for l in list]

def noop(x):
    pass

def createRider(square, lane):
    return Rider("Tac", Cards([], noop), riderMove.Rider(square, lane))

class SimplePlayer():
    def __init__(self, riders, move):
        self.riders = riders
        self.move = move

    def pickNextMoves(self):
        for r in self.riders:
            r.nextMove = self.move


from obstacles import Obstacles
from obstacles import Obstacles
from slipstreaming import slipstreaming
from exhaust import exhaust

class Race():
    def __init__(self, track, riders, players, logger):
        self.track = track
        self.riders = riders
        self.obstacles = Obstacles(riders)
        self.players = players
        self.arrivals = []
        self.logger = logger
        self.checkArrivals()

    def isOver(self):
        return not self.riders

    def newTurn(self):
        for p in self.players:
            p.pickNextMoves()

        for r in headToTail(self.riders):
            start = r.position()
            r.move(r.nextMove, self.track, self.obstacles)
            self.logger.logMove(r, start, r.position(), self.obstacles)

        slipstreaming(self.riders, self.track, self.logger)
        self.checkArrivals()

        exhaust(headToTail(self.riders), self.logger)

    def ranking(self):
        return self.arrivals

    def checkArrivals(self):
        for r in headToTail(self.riders):
            if arrived(r, self.track):
                self.riders.remove(r)
                self.arrivals.append(r)
                self.removeFromPlayers(r)

    def removeFromPlayers(self, rider):
        for p in self.players:
            if rider in p.riders:
                p.riders.remove(rider)


def arrived(rider, track):
    return track.getRoadType(rider.getSquare()) == "end"

def headToTail(riders):
    return sorted(riders, key = absolutePosition, reverse = True)

def absolutePosition(rider):
    square, lane = rider.position()
    return 2*square + 1 - lane

if __name__ == "__main__":
    tests()
