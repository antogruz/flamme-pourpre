#!/usr/bin/env python3

from unittests import Tester, assert_equals
from track import Track
from riderMove import Rider

def tests():
    GameTest().runTests()

class GameTest(Tester):
    def __init__(self):
        self.track = Track([(5, "normal"), (2, "end")])

    def createGame(self, riders):
        return Game(self.track, riders)

    def testCreateGame(self):
        riders = [Rider(0, 0)]
        game = self.createGame(riders)
        assert_equals(False, game.isOver())

    def testGameOver(self):
        game = self.createGame([])
        assert_equals(True, game.isOver())

    def testGameIsOverIfAllRidersHavePassedLine(self):
        game = self.createGame([Rider(5, 0)])
        assert_equals(True, game.isOver())

    def testRiderMovesAfterATurn(self):
        rider = Rider(0, 0)
        game = self.createGame([rider])
        rider.nextMove = 1
        game.newTurn()
        assert_equals(1, rider.position()[0])



from riders import Riders
class Game():
    def __init__(self, track, riders):
        self.track = track
        self.riders = riders
        self.obstacles = Riders(riders)

    def isOver(self):
        for r in self.riders:
            if self.track.getRoadType(r.position()[0]) != "end":
                return False
        return True

    def newTurn(self):
        for r in self.riders:
            r.move(r.nextMove, self.track, self.obstacles)



if __name__ == "__main__":
    tests()
