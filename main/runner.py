#!/usr/bin/env python3

from tracks import *
from race import Race
import riderMove
import random
from tokensDecorators import TokensDecorators
from trackDisplay import TrackDisplay
from tkinterSpecific.canvasBoxFactory import CanvasBoxFactory
from animation import EventAnimator, RoadAnimator
from raceLayout import RaceLayout
from menu import *
from ridersFactory import *
from eventDisplay import EventDisplay
from results import displayResults
from frames import Frames
from cols import getPointsForClimbs
from meilleurGrimpeurObserver import createClimberObserver
from decorators.miniracePointsDisplay import MiniRacePointsDisplay
from decorators.riderDisplay import RidersDisplay
from decorators.rankingDisplay import RankingDisplay
from intermediateSprintObserver import createSprintObserver, getPointsForSprints

def noLog(ranking):
    pass

class SpecialModes:
    def __init__(self, bestClimber, intermediateSprint):
        self.bestClimber = bestClimber
        self.intermediateSprint = intermediateSprint

class Runner:
    def __init__(self, window, clock, displayers = []):
        self.window = window
        self.clock = clock
        self.displayers = displayers

    def runTour(self, tour, tracks):
        for track in tracks:
            tour.newRace()
            self.runRace(track, tour.teams, tour.checkNewArrivals, SpecialModes(True, True))
            clear(self.window)
            frames = Frames(self.window)
            displayResults(frames.new(), tour.scores(), tour.times(), tour.climberPoints())
            createSimpleMenu(frames.new(), ["Next Race!"])
            clear(self.window)

    def runRace(self, track, teams, logRanking = noLog, modes = SpecialModes(False, False)):
        for team in teams:
            team.player.resetRiders(team.riders)
        riders = allRiders(teams)
        players = allPlayers(teams)
        for rider in riders:
            rider.cards.newRace()

        layout = RaceLayout(self.window)
        tokensDecorators, eventAnimator, roadAnimator = createDisplays(track, layout, self.clock)
        raceDisplayers = self.displayers + [tokensDecorators]
        setRidersOnStart(riders)
        tokensDecorators.addRoadDecorator(RidersDisplay(riders, tokensDecorators.trackDisplay))
        race = Race(track, riders, players)
        tokensDecorators.addRoadDecorator(RankingDisplay(race, tokensDecorators.trackDisplay))
        race.addObserver(eventAnimator)
        race.addObserver(roadAnimator)
        if modes.bestClimber:
            createMiniRaces(tokensDecorators, race, createClimbsObservers(track), "red")
        if modes.intermediateSprint:
            createMiniRaces(tokensDecorators, race, createSprintsObservers(track), "green")

        for d in raceDisplayers:
            d.update()

        while not race.isOver():
            race.newTurn()
            logRanking(race.ranking())
            for d in raceDisplayers:
                d.update()

def allRiders(teams):
    return [rider for team in teams for rider in team.riders]

def allPlayers(teams):
    return [team.player for team in teams]

def createMiniRaces(tokensDecorators, race, observers, decoratorColor):
    for observer in observers:
        race.addObserver(observer)
        tokensDecorators.addRoadDecorator(MiniRacePointsDisplay(observer, decoratorColor, tokensDecorators.trackDisplay))

def createClimbsObservers(track):
    return [ createClimberObserver(lastAscentSquare, points) for (points, lastAscentSquare) in getPointsForClimbs(track) ]

def createSprintsObservers(track):
    return [ createSprintObserver(lastSquare, points) for (lastSquare, points) in getPointsForSprints(track) ]


def createDisplays(track, layout, clock):
    factory = CanvasBoxFactory(layout.getTrackFrame())
    trackDisplay = TrackDisplay(factory, track)
    eventDisplay = EventDisplay(layout.getEventFrame())
    eventAnimator = EventAnimator(eventDisplay)
    roadAnimator = RoadAnimator(layout.getTrackFrame(), trackDisplay, track, clock)
    tokensDecorators = TokensDecorators(layout.getTrackFrame(), trackDisplay)
    return tokensDecorators, eventAnimator, roadAnimator


def setRidersOnStart(riders):
    random.shuffle(riders)
    square, lane = 0, 0
    for r in riders:
        r.riderMove = riderMove.Rider(square, lane)
        square, lane = next(square, lane)

def next(square, lane):
    if lane == 0:
        return square, lane + 1
    return square + 1, 0


def pickTrack(window):
    trackCreator = createMenu(window, [("Corso Paseo", corsoPaseo), ("Col du ballon", colDuBallon), ("Haute Montagne", hauteMontagne), ("Classicissima", classicissima), ("Ronde Van Wevelgem", rondeVanWevelgem), ("Firenze-Milano", firenzeMilano)])
    return trackCreator()


