#! /usr/bin/env python3

from track import streamable

class RiderInRace():
    def __init__(self, rider, square, lane):
        self.persistent = rider
        self.name = rider.name
        self.shade = rider.shade
        self.color = rider.color
        self.square = square
        self.lane = lane
        self.arrived = False

    def position(self):
        return (self.square, self.lane)

    def getSquare(self):
        return self.square

    def move(self, fuel, track, obstacles):
        self.square, self.lane = self.persistent.movementRules.computeNewPosition(self.position(), fuel, track, obstacles)

    def getSlipstream(self, track):
        if not streamable(track.getRoadType(self.square)):
            return False

        self.square += 1
        return True

    def exhaust(self):
        self.persistent.propulsor.exhaust()

    def setArrived(self):
        self.arrived = True

    def addTime(self, time):
        self.persistent.time += time

    def earnScore(self, score):
        self.persistent.score += score

from unittests import *
from riderBuilder import RiderBuilder

class IntegrationTester():
    def testEmptyDeck(self):
        builder = RiderBuilder()
        builder.buildOracle(ChoiceDoer([0, 0, 0]))
        builder.buildDeck([])
        rider = RiderInRace(builder.getResult(), 0, 0)
        assert_equals(2, rider.persistent.propulsor.generateMove())

    def testOpportunistic(self):
        builder = RiderBuilder()
        builder.buildOracle(ChoiceDoer([0, 2]))
        builder.buildOpportunisticDeck([5], ["magenta"], noop)
        rider = RiderInRace(builder.getResult(), 0, 0)
        assert_equals(5, rider.persistent.propulsor.generateMove())

class ChoiceDoer():
    def __init__(self, future):
        self.future = future

    def pick(self, possibilities, *_):
        return self.future.pop(0)

def noop(*_):
    pass

if __name__ == "__main__":
    runTests(IntegrationTester())

