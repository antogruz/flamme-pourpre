#!/usr/bin/env python3

from unittests import *

class Tour:
    def __init__(self, teams):
        self.teams = teams
        for t in teams:
            t.score = 0

    def scores(self):
        return [(team.color, team.score) for team in self.teams]

    def checkNewArrivals(self, ranking):
        for rider in ranking:
            self.findTeam(rider).score += 3

    def findTeam(self, rider):
        for team in self.teams:
            if rider in team.riders:
                return team



class TourTest:
    def testScoreAtBeginning(self):
        tour = Tour([Team("green", [])])
        assert_equals([("green", 0)], tour.scores())

    def testMultipleTeamsScore(self):
        tour = Tour([Team("green"), Team("blue")])
        assert_similars([("green", 0), ("blue", 0)], tour.scores())

    def testScoresAfterARace(self):
        rider = Rider()
        tour = Tour([Team("green", [rider])])
        tour.checkNewArrivals([rider])
        assert_similars([("green", 3)], tour.scores())


class Team:
    def __init__(self, color, riders = []):
        self.color = color
        self.riders = riders

class Rider:
    pass

if __name__ == "__main__":
    runTests(TourTest())

