#!/usr/bin/env python3

from jeu.tracks import *
from race import Race
import riderMove
import random
from tokensDecorators import TokensDecorators
from trackDisplay import TrackDisplay
from tkinterSpecific.canvasBoxFactory import CanvasBoxFactory
from animation import EventAnimator, RoadAnimator
from raceLayout import RaceLayout
from menu import *
from eventDisplay import EventDisplay
from results import displayResults
from beau.resultsWindow import ResultsWindow
from frames import Frames
from cols import getPointsForClimbs
from meilleurGrimpeurObserver import createClimberObserver
from decorators.miniracePointsDisplay import MiniRacePointsDisplay
from decorators.riderDisplay import RidersDisplay
from decorators.rankingDisplay import RankingDisplay
from intermediateSprintObserver import createSprintObserver, getPointsForSprints
from race import TeamInRace
from specialTour.extendTrack import extendTrack

def noLog(ranking):
    pass

class SpecialModes:
    def __init__(self, bestClimber=None, intermediateSprint=None):
        self.bestClimber = bestClimber
        self.intermediateSprint = intermediateSprint

class Runner:
    def __init__(self, window, clock, displayers = []):
        self.window = window
        self.clock = clock
        self.displayers = displayers

    def runTour(self, tour, tracksBuilders, appearances, bonusPerRace = 0):
        self.displayers.append(ResultsWindow(self.window, tour, appearances))
        bonusSquares = 0
        for trackBuilder in tracksBuilders:
            track = extendTrack(trackBuilder(len(tour.teams)), bonusSquares)
            tour.newRace()
            self.runRace(track, tour.teams, tour.checkNewArrivals,
                         SpecialModes(bestClimber=tour.addClimberPoints,
                                      intermediateSprint=tour.addPoints),
                         appearances)
            for team in tour.teams:
                team.progression.progress()
            bonusSquares += bonusPerRace


    def runRace(self, track, teams, logRanking = noLog, modes = SpecialModes(), appearances = None):
        teamsInRace = [TeamInRace(team) for team in teams]
        setRidersOnStart(teamsInRace)
        riders = [rider for team in teamsInRace for rider in team.ridersInRace]
        for rider in riders:
            rider.personnage.propulsor.newRace()

        layout = RaceLayout(self.window)
        tokensDecorators, eventAnimator, roadAnimator = createDisplays(track, layout, self.clock, appearances)
        raceDisplayers = self.displayers + [tokensDecorators]
        tokensDecorators.addRoadDecorator(RidersDisplay(riders, tokensDecorators.trackDisplay, appearances))
        race = Race(track, teamsInRace)
        tokensDecorators.addRoadDecorator(RankingDisplay(race, tokensDecorators.trackDisplay, appearances))
        race.addObserver(eventAnimator)
        race.addObserver(roadAnimator)
        if modes.bestClimber:
            createMiniRaces(tokensDecorators, race, createClimbsObservers(track, modes.bestClimber), "red")
        if modes.intermediateSprint:
            createMiniRaces(tokensDecorators, race, createSprintsObservers(track, modes.intermediateSprint), "green")

        for d in raceDisplayers:
            d.update()

        while not race.isOver():
            race.newTurn()
            logRanking(race.ranking())
            for d in raceDisplayers:
                d.update()

def createMiniRaces(tokensDecorators, race, observers, decoratorColor):
    for observer in observers:
        race.addObserver(observer)
        tokensDecorators.addRoadDecorator(MiniRacePointsDisplay(observer, decoratorColor, tokensDecorators.trackDisplay))

def createClimbsObservers(track, awardClimberPoints):
    return [ createClimberObserver(lastAscentSquare, points, awardClimberPoints) for (points, lastAscentSquare) in getPointsForClimbs(track) ]

def createSprintsObservers(track, awardPoints):
    return [ createSprintObserver(lastSquare, points, awardPoints) for (lastSquare, points) in getPointsForSprints(track) ]


def createDisplays(track, layout, clock, appearances):
    factory = CanvasBoxFactory(layout.getTrackFrame())
    trackDisplay = TrackDisplay(factory, track)
    eventDisplay = EventDisplay(layout.getEventFrame(), appearances)
    eventAnimator = EventAnimator(eventDisplay)
    roadAnimator = RoadAnimator(layout.getTrackFrame(), trackDisplay, track, appearances, clock)
    tokensDecorators = TokensDecorators(layout.getTrackFrame(), trackDisplay)
    return tokensDecorators, eventAnimator, roadAnimator


def setRidersOnStart(teamsInRace):
    teamsWithRidersWaiting = list(teamsInRace)
    random.shuffle(teamsWithRidersWaiting)
    square, lane = 0, 0
    while teamsWithRidersWaiting:
        team = teamsWithRidersWaiting[0]
        if team.placeNextRider(square, lane):
            square, lane = next(square, lane)
        else:
            teamsWithRidersWaiting.pop(0)

def next(square, lane):
    if lane == 0:
        return square, lane + 1
    return square + 1, 0


def pickTrack(window):
    trackCreator = createMenu(window, [("Corso Paseo", corsoPaseo), ("Col du ballon", colDuBallon), ("Haute Montagne", hauteMontagne), ("Classicissima", classicissima), ("Ronde Van Wevelgem", rondeVanWevelgem), ("Firenze-Milano", firenzeMilano)])
    return trackCreator()


