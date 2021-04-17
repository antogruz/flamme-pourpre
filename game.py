#!/usr/bin/env python3

from unittests import Tester, assert_equals
from track import Track
from rider import Rider
from cards import Cards
import riderMove

def tests():
    GameTest().runTests()

class GameTest(Tester):
    def __init__(self):
        self.track = Track([(5, "normal"), (2, "end")])

    def createGame(self, riders):
        return Game(self.track, riders, [SimplePlayer(riders, 2)])

    def testCreateGame(self):
        riders = [createRider(0, 0)]
        game = self.createGame(riders)
        assert_equals(False, game.isOver())

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

    def isOver(self):
        for r in self.riders:
            if self.track.getRoadType(r.position()[0]) != "end":
                return False
        return True

    def newTurn(self):
        for p in self.players:
            p.pickNextMoves()

        for r in headToTail(self.riders):
            r.move(r.nextMove, self.track, self.obstacles)

        slipstreaming(self.riders, self.track)
        exhaust(self.riders)


def headToTail(riders):
    return sorted(riders, key = absolutePosition, reverse = True)

def absolutePosition(rider):
    square, lane = rider.position()
    return 2*square + 1 - lane

if __name__ == "__main__":
    tests()
