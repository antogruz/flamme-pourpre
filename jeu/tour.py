#!/usr/bin/env python3

from unittests import *

class Tour:
    def __init__(self, teams):
        self.teams = teams
        for t in teams:
            t.score = 0
        self.bounty = 3
        self.alreadyArrived = []

    def scores(self):
        return [(team.color, team.score) for team in sorted(self.teams, key = getScore, reverse = True)]

    def checkNewArrivals(self, ranking):
        newArrivals = self.extractNew(ranking)
        for rider in newArrivals:
            self.findTeam(rider).score += self.claimBounty()

    def findTeam(self, rider):
        for team in self.teams:
            if rider in team.riders:
                return team

    def claimBounty(self):
        if self.bounty == 0:
            return 0
        self.bounty -= 1
        return self.bounty + 1

    def extractNew(self, ranking):
        newOnes = [rider for rider in ranking if rider not in self.alreadyArrived]
        self.alreadyArrived = ranking
        return newOnes


def getScore(team):
    return team.score

class TourTest:
    def __before__(self):
        self.a, self.b, self.c, self.d = Rider(), Rider(), Rider(), Rider()
        self.green = Team("green", [self.a, self.b])
        self.blue = Team("blue", [self.c, self.d])

    def testScoreAtBeginning(self):
        tour = Tour([self.green])
        assert_equals([("green", 0)], tour.scores())

    def testMultipleTeamsScore(self):
        tour = Tour([self.green, self.blue])
        assert_similars([("green", 0), ("blue", 0)], tour.scores())

    def testFirstGets3Points(self):
        tour = Tour([self.green])
        tour.checkNewArrivals([self.a])
        assert_similars([("green", 3)], tour.scores())

    def testScoresAfterARace(self):
        tour = Tour([self.green, self.blue])
        tour.checkNewArrivals([self.a, self.b, self.c, self.d])
        assert_similars([("green", 5), ("blue", 1)], tour.scores())

    def testArrivalsInDifferentTurns(self):
        tour = Tour([self.green, self.blue])
        tour.checkNewArrivals([self.a])
        tour.checkNewArrivals([self.a, self.c, self.b])
        tour.checkNewArrivals([self.a, self.c, self.b, self.d])
        assert_similars([("green", 4), ("blue", 2)], tour.scores())

    def testScoresInDescendingOrder(self):
        tour = Tour([self.green, self.blue])
        tour.checkNewArrivals([self.c, self.d, self.a, self.b])
        assert_equals([("blue", 5), ("green", 1)], tour.scores())


class Team:
    def __init__(self, color, riders = []):
        self.color = color
        self.riders = riders

class Rider:
    pass

if __name__ == "__main__":
    runTests(TourTest())

