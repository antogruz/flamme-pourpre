#!/usr/bin/env python3

from unittests import Tester, assert_equals, assert_similars
from track import Track
from rider import Rider
from cards import Cards
import riderMove

def tests():
    GameTest().runTests()

class GameTest(Tester):
    def __init__(self):
        self.track = Track([(5, "normal"), (3, "end")])

    def createGame(self, riders):
        return Game(self.track, riders, [SimplePlayer(copy(riders), 2)])

    def testCreateGame(self):
        riders = [createRider(0, 0)]
        game = self.createGame(riders)
        assert_equals(False, game.isOver())
        assert_similars([], game.ranking())

    def testGameOver(self):
        game = self.createGame([])
        assert_equals(True, game.isOver())

    def testGameIsOverIfAllRidersHavePassedLine(self):
        game = self.createGame([createRider(5, 0)])
        assert_equals(True, game.isOver())

    def testRiderMovesAfterATurn(self):
        rider = createRider(0, 0)
        game = self.createGame([rider])
        game.newTurn()
        assert_equals(2, rider.position()[0])

    def testArrival(self):
        rider = createRider(4, 0)
        game = self.createGame([rider, createRider(0, 0)])
        game.newTurn()
        assert_similars([rider], game.ranking())

    def testDontPlayForArrivedRiders(self):
        rider = createRider(5, 0)
        rider.nextMove = 100
        game = self.createGame([rider])
        game.newTurn()
        assert_equals(100, rider.nextMove)

    def testRanking(self):
        first = createRider(5, 0)
        second = createRider(4, 0)
        third = createRider(3, 0)
        fourth = createRider(0, 0)
        game = self.createGame([fourth, second, third, first])
        while not game.isOver():
            game.newTurn()
        assert_equals([first, second, third, fourth], game.ranking())


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

class Game():
    def __init__(self, track, riders, players):
        self.track = track
        self.riders = riders
        self.obstacles = Obstacles(riders)
        self.players = players
        self.arrivals = []
        self.checkArrivals()

    def isOver(self):
        return not self.riders

    def newTurn(self):
        for p in self.players:
            p.pickNextMoves()

        for r in headToTail(self.riders):
            r.move(r.nextMove, self.track, self.obstacles)

        slipstreaming(self.riders, self.track)
        self.checkArrivals()

        exhaust(self.riders)

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
