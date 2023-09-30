#!/usr/bin/env python3

from tracks import *
from race import Race
import riderMove
import random
from display import RoadDisplay
from animation import Logger, Animation, EventAnimator, RoadAnimator
from raceLayout import RaceLayout
from cardsDisplay import CardsDisplay
from menu import *
from ridersFactory import *
from eventDisplay import EventDisplay
from results import displayResults
from frames import Frames
from cols import getPointsForClimbs
from meilleurGrimpeurObserver import createClimberObserver
from miniracePointsDisplay import MiniRacePointsDisplay
from riderDisplay import RidersDisplay
from rankingDisplay import RankingDisplay
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
        roadDisplay, animation = createDisplays(track, layout, self.clock)
        raceDisplayers = self.displayers + [roadDisplay]
        setRidersOnStart(riders)
        roadDisplay.addRoadDecorator(RidersDisplay(riders))
        race = Race(track, riders, players)
        roadDisplay.addRoadDecorator(RankingDisplay(race))
        logger = Logger()
        race.addObserver(logger)
        if modes.bestClimber:
            createMiniRaces(roadDisplay, race, createClimbsObservers(track), "red")
        if modes.intermediateSprint:
            createMiniRaces(roadDisplay, race, createSprintsObservers(track), "green")

        for d in raceDisplayers:
            d.update()

        while not race.isOver():
            race.newTurn()
            animation.animate(logger.getMoves(), logger.getGroups(), logger.getExhausted())
            logRanking(race.ranking())
            for d in raceDisplayers:
                d.update()
            logger.__init__()

def allRiders(teams):
    return [rider for team in teams for rider in team.riders]

def allPlayers(teams):
    return [team.player for team in teams]

def createMiniRaces(roadDisplay, race, observers, decoratorColor):
    for observer in observers:
        race.addObserver(observer)
        roadDisplay.addRoadDecorator(MiniRacePointsDisplay(observer, decoratorColor))

def createClimbsObservers(track):
    return [ createClimberObserver(lastAscentSquare, points) for (points, lastAscentSquare) in getPointsForClimbs(track) ]

def createSprintsObservers(track):
    return [ createSprintObserver(lastSquare, points) for (lastSquare, points) in getPointsForSprints(track) ]


def createDisplays(track, layout, clock):
    roadDisplay = RoadDisplay(layout.getTrackFrame(), track)
    eventDisplay = EventDisplay(layout.getEventFrame())
    animation = Animation([EventAnimator(eventDisplay), RoadAnimator(roadDisplay, clock)], clock)
    return roadDisplay, animation


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


