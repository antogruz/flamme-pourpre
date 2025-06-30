#! /usr/bin/env python3

from team import Team

class TeamBuilder:
    def __init__(self):
        self.riders = []
        self.color = None
        self.propulsion = None
        self.oracle = None

    def buildColor(self, color):
        self.color = color

    def addRider(self, rider):
        self.riders.append(rider)

    def buildPropulsion(self, propulsion):
        self.propulsion = propulsion

    def buildOracle(self, oracle):
        self.oracle = oracle

    def getResult(self):
        for rider in self.riders:
            rider.color = self.color
        return Team(self.color, self.riders, self.propulsion, self.oracle)