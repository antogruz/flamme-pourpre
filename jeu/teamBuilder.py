#! /usr/bin/env python3

from team import Team

class TeamBuilder:
    def __init__(self):
        self.riders = []
        self.propulsion = None
        self.oracle = None

    def addRider(self, rider):
        self.riders.append(rider)

    def buildPropulsion(self, propulsion):
        self.propulsion = propulsion

    def buildOracle(self, oracle):
        self.oracle = oracle

    def getResult(self):
        return Team(self.riders, self.propulsion, self.oracle)