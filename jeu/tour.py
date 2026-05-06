#!/usr/bin/env python3

from unittests import *
from timer import Timer
# Cette classe implémente les règles du grand tour. Elle sera changée si l'on ajoute des points pour les meilleurs grimpeurs par exemple, ou si on change la répartition des gains pour les gagnants d'une étape.

class Tour:
    def __init__(self, teams):
        self.teams = teams
        self.times = {rider: 0 for rider in self.getRiders()}
        self.points = {rider: 0 for rider in self.getRiders()}
        self.climberPoints = {rider: 0 for rider in self.getRiders()}
        self.newRace()

    def getScores(self):
        pointsForEachTeam = {team: 0 for team in self.teams}
        for team in self.teams:
            pointsForEachTeam[team] = sum([self.points[rider] for rider in team.riders])
        return [(team.color, points) for team, points in sortDictByValue(pointsForEachTeam, reverse = True)]

    def ridersResults(self):
        self.shiftTimesTowardZero()
        riders = sortDictByValue(self.times)
        return [{
            'rider': rider,
            'time': self.times[rider],
            'score': self.points[rider],
            'climberPoints': self.climberPoints[rider]
        } for rider, _ in riders]

    def checkNewArrivals(self, ranking):
        newArrivals = self.extractNew(ranking)
        for rider in newArrivals:
            self.addPoints(rider.personnage, self.claimBounty())
        self.timer.arrive(newArrivals)
        for rider in newArrivals:
            self.times[rider.personnage] += self.timer.getRaceTime(rider)

    def addPoints(self, rider, points):
        self.points[rider] += points

    def addClimberPoints(self, rider, points):
        self.climberPoints[rider] += points

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

    def getTimes(self):
        self.shiftTimesTowardZero()
        return sortDictByValue(self.times)

    def shiftTimesTowardZero(self):
        bestTime = min(self.times.values())
        for rider in self.times:
            self.times[rider] -= bestTime

    def getClimberPoints(self):
        return [(rider, points) for rider, points in sortDictByValue(self.climberPoints, reverse = True) if points > 0]

    def getRiders(self):
        return [rider for team in self.teams for rider in team.riders]

def sortDictByValue(dict, reverse = False):
    return sorted(dict.items(), key = lambda x: x[1], reverse = reverse)

def copy(l):
    return [e for e in l]



class TourTest:
    def __before__(self):
        self.a, self.b, self.c, self.d = Rider("a"), Rider("b"), Rider("c"), Rider("d")
        self.green = Team("green", [self.a, self.b])
        self.blue = Team("blue", [self.c, self.d])

    def testScoreAtBeginning(self):
        tour = Tour([self.green])
        assert_equals([("green", 0)], tour.getScores())

    def testMultipleTeamsScore(self):
        tour = Tour([self.green, self.blue])
        assert_similars([("green", 0), ("blue", 0)], tour.getScores())

    def testFirstGets3Points(self):
        tour = Tour([self.green])
        tour.checkNewArrivals([self.a])
        assert_similars([("green", 3)], tour.getScores())

    def testScoresAfterARace(self):
        tour = Tour([self.green, self.blue])
        tour.checkNewArrivals([self.a, self.b, self.c, self.d])
        assert_similars([("green", 5), ("blue", 1)], tour.getScores())

    def testArrivalsInDifferentTurns(self):
        tour = Tour([self.green, self.blue])
        tour.checkNewArrivals([self.a])
        tour.checkNewArrivals([self.a, self.c, self.b])
        tour.checkNewArrivals([self.a, self.c, self.b, self.d])
        assert_similars([("green", 4), ("blue", 2)], tour.getScores())

    def testScoresInDescendingOrder(self):
        tour = Tour([self.green, self.blue])
        tour.checkNewArrivals([self.c, self.d, self.a, self.b])
        assert_equals([("blue", 5), ("green", 1)], tour.getScores())

    def testTwoRaces(self):
        tour = Tour([self.green])
        tour.checkNewArrivals([self.a])
        tour.newRace()
        tour.checkNewArrivals([self.a])
        assert_equals([("green", 6)], tour.getScores())

    def testTimes(self):
        tour = Tour([self.green, self.blue])
        self.c.pos = 1
        self.b.pos = 2
        tour.checkNewArrivals([self.a])
        tour.checkNewArrivals([self.c, self.d])
        tour.checkNewArrivals([self.b])
        assert_equals([(self.a, 0), (self.c, 50), (self.d, 60), (self.b, 100)], tour.getTimes())

    def testTwoRacesTimes(self):
        tour = Tour([self.green, self.blue])
        tour.checkNewArrivals([self.a])
        tour.checkNewArrivals([self.b, self.c, self.d])
        tour.newRace()
        tour.checkNewArrivals([self.b])
        tour.checkNewArrivals([self.a, self.c, self.d])
        assert_similars([(self.a, 0), (self.b, 0), (self.c, 60), (self.d, 60)], tour.getTimes())

    def testArrivalsIsCopied(self):
        tour = Tour([self.green])
        arrivals = [self.a]
        tour.checkNewArrivals(arrivals)
        arrivals.append(self.b)
        tour.checkNewArrivals(arrivals)
        assert_equals([("green", 5)], tour.getScores())

    def testRidersResults(self):
        tour = Tour([self.green])
        tour.checkNewArrivals([self.a])
        assert_equals(2, len(tour.ridersResults()))

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
        self.personnage = self

    def position(self):
        return self.pos, 0

if __name__ == "__main__":
    runTests(TourTest())

