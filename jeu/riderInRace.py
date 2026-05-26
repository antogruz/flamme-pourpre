#! /usr/bin/env python3


class RiderInRace():
    def __init__(self, rider, square, lane):
        self.personnage = rider
        self.square = square
        self.lane = lane

    def position(self):
        return (self.square, self.lane)

    def getSquare(self):
        return self.square

    def move(self, fuel, track, obstacles):
        self.square, self.lane = self.personnage.movementRules.computeNewPosition(self.position(), fuel, track, obstacles)

    def earnSquares(self, distance, track, obstacles):
        self.square, self.lane = self.personnage.movementRules.findAvailableSlot(obstacles, self.position(), distance, track)

    def exhaust(self):
        self.personnage.propulsor.exhaust()

from unittests import *
from riderBuilder import RiderBuilder

class IntegrationTester():
    def testEmptyDeck(self):
        builder = RiderBuilder()
        builder.buildOracle(ChoiceDoer([0, 0, 0]))
        builder.buildDeck([])
        rider = RiderInRace(builder.getResult(), 0, 0)
        move = rider.personnage.propulsor.generateMove()
        assert_equals("", move.label())
        assert_equals(2, move.energy())

    def testOpportunistic(self):
        builder = RiderBuilder()
        builder.buildOracle(ChoiceDoer([0, 2]))
        builder.buildOpportunisticDeck([5], ["magenta"], noop)
        rider = RiderInRace(builder.getResult(), 0, 0)
        assert_equals(5, rider.personnage.propulsor.generateMove().energy())

class ChoiceDoer():
    def __init__(self, future):
        self.future = future

    def pick(self, possibilities, *_):
        return self.future.pop(0)

def noop(*_):
    pass

if __name__ == "__main__":
    runTests(IntegrationTester())

