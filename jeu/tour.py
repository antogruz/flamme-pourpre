#!/usr/bin/env python3

from unittests import *
from timer import Timer
# Cette classe implémente les règles du grand tour. Elle sera changée si l'on ajoute des points pour les meilleurs grimpeurs par exemple, ou si on change la répartition des gains pour les gagnants d'une étape.

class Tour:
    def __init__(self, teams):
        self.teams = teams
        for t in teams:
            for r in t.riders:
                r.time = 0
                r.score = 0
                r.climberPoints = 0
        self.newRace()

    def scores(self):
        return [(team.color, team.score()) for team in sorted(self.teams, key = getScore, reverse = True)]

    def ridersResults(self):
        riders = sorted(self.getRiders(), key = getTime)
        removeTime(riders[0].time, riders)
        return [{
            'name': rider.name,
            'color': self.findTeam(rider).color,
            'time': rider.time,
            'score': rider.score,
            'climberPoints': rider.climberPoints
        } for rider in riders]

    def checkNewArrivals(self, ranking):
        newArrivals = self.extractNew(ranking)
        for rider in newArrivals:
            rider.earnScore(self.claimBounty())
        self.timer.arrive(newArrivals)

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
        self.alreadyArrived = copy(ranking)
        return newOnes

    def newRace(self):
        self.bounty = 3
        self.alreadyArrived = []
        self.timer = Timer()

    def times(self):
        riders = sorted(self.getRiders(), key = getTime)
        removeTime(riders[0].time, riders)
        return [(self.findTeam(rider).color + " " + rider.name, rider.time) for rider in riders]

    def climberPoints(self):
        riders = sorted(self.getRiders(), key = getClimberPoints, reverse = True)
        return [(self.findTeam(rider).color + " " + rider.name, getClimberPoints(rider)) for rider in riders if getClimberPoints(rider) > 0]

    def getRiders(self):
        return [rider for team in self.teams for rider in team.riders]

def removeTime(delta, riders):
    for r in riders:
        r.time -= delta


def copy(l):
    return [e for e in l]

def getScore(team):
    return team.score()

def getTime(rider):
    return rider.time

def getClimberPoints(rider):
    return rider.climberPoints



class TourTest:
    def __before__(self):
        self.a, self.b, self.c, self.d = Rider("a"), Rider("b"), Rider("c"), Rider("d")
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

    def testTwoRaces(self):
        tour = Tour([self.green])
        tour.checkNewArrivals([self.a])
        tour.newRace()
        tour.checkNewArrivals([self.a])
        assert_equals([("green", 6)], tour.scores())

    def testTimes(self):
        tour = Tour([self.green, self.blue])
        self.c.pos = 1
        self.b.pos = 2
        tour.checkNewArrivals([self.a])
        tour.checkNewArrivals([self.c, self.d])
        tour.checkNewArrivals([self.b])
        assert_equals([("green a", 0), ("blue c", 50), ("blue d", 60), ("green b", 100)], tour.times())

    def testTwoRacesTimes(self):
        tour = Tour([self.green, self.blue])
        tour.checkNewArrivals([self.a])
        tour.checkNewArrivals([self.b, self.c, self.d])
        tour.newRace()
        tour.checkNewArrivals([self.b])
        tour.checkNewArrivals([self.a, self.c, self.d])
        assert_similars([("green a", 0), ("green b", 0), ("blue c", 60), ("blue d", 60)], tour.times())

    def testArrivalsIsCopied(self):
        tour = Tour([self.green])
        arrivals = [self.a]
        tour.checkNewArrivals(arrivals)
        arrivals.append(self.b)
        tour.checkNewArrivals(arrivals)
        assert_equals([("green", 5)], tour.scores())


class Team:
    def __init__(self, color, riders = []):
        self.color = color
        self.riders = riders
        for r in self.riders:
            r.color = color

    def score(self):
        return sum([r.score for r in self.riders])

class Rider:
    def __init__(self, name, position = 0):
        self.name = name
        self.pos = position
        self.score = 0

    def position(self):
        return self.pos, 0

    def earnScore(self, score):
        self.score += score

    def addTime(self, time):
        self.time += time

if __name__ == "__main__":
    runTests(TourTest())

