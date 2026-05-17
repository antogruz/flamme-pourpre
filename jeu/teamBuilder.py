#! /usr/bin/env python3

from team import Team, TeamProgression

class TeamBuilder:
    def __init__(self):
        self.riders = []
        self.propulsion = None
        self.oracle = None
        self.progression = TeamProgression()

    def addRider(self, rider):
        self.riders.append(rider)

    def buildPropulsion(self, propulsion):
        self.propulsion = propulsion

    def buildOracle(self, oracle):
        self.oracle = oracle

    def buildProgression(self, progression):
        self.progression = progression

    def getResult(self):
        return Team(self.riders, self.propulsion, self.oracle, self.progression)