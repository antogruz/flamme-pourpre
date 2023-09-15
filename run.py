#!/usr/bin/env python3

import tkinter as tk
from track import Track
from tracks import *
from player import Player
from race import Race
from cards import Cards
import riderMove
import random
from display import RoadDisplay
from animation import Logger, CardDecorator, Animation, EventAnimator, RoadAnimator
from raceLayout import RaceLayout
from cardsDisplay import CardsDisplay
from menu import *
from tour import Tour, Team
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

def integrationTests():
    window = tk.Tk()
    runner = Runner(window, 0.003, 0)
    twoRacesSprinteursOnly(runner)
    clear(window)
    integrationSingle(runner)
    window.mainloop()

def integrationSingle(runner):
    teams = [ createBot(color) for color in ["green", "red", "blue", "black", "magenta"] ]
    runner.runRace(colDuBallon(), teams)

def allRiders(teams):
    return [rider for team in teams for rider in team.riders]

def allPlayers(teams):
    return [team.player for team in teams]

def noLog(ranking):
    pass

def twoRacesSprinteursOnly(runner):
    teams = [ sprinteurOnlyTeam(color) for color in ["blue", "red", "black"] ]
    for team in teams:
        team.player = createBotPlayer(team)
    tour = Tour(teams)
    runner.runTour(tour, [corsoPaseo(), firenzeMilano()])

class SpecialModes:
    def __init__(self, bestClimber, intermediateSprint):
        self.bestClimber = bestClimber
        self.intermediateSprint = intermediateSprint

class Runner:
    def __init__(self, window, clock, decksDisplayed):
        self.window = window
        self.clock = clock
        self.decksDisplayed = decksDisplayed

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

        layout = RaceLayout(self.window, decksCount = self.decksDisplayed)
        displays, animation = createDisplays(track, layout, self.clock, self.window, riders[0:self.decksDisplayed])
        setRidersOnStart(riders)
        displays.roadDisplay.addRoadDecorator(RidersDisplay(riders))
        race = Race(track, riders, players)
        displays.roadDisplay.addRoadDecorator(RankingDisplay(race))
        logger = Logger()
        race.addObserver(logger)
        if modes.bestClimber:
            createMiniRaces(displays.roadDisplay, race, createClimbsObservers(track), "red")
        if modes.intermediateSprint:
            createMiniRaces(displays.roadDisplay, race, createSprintsObservers(track), "green")

        displays.update(riders, race)

        while not race.isOver():
            race.newTurn()
            animation.animate(logger.getMoves(), logger.getGroups(), logger.getExhausted())
            logRanking(race.ranking())
            displays.update(riders, race)
            logger.__init__()


def createMiniRaces(roadDisplay, race, observers, decoratorColor):
    for observer in observers:
        race.addObserver(observer)
        roadDisplay.addRoadDecorator(MiniRacePointsDisplay(observer, decoratorColor))

def createClimbsObservers(track):
    return [ createClimberObserver(lastAscentSquare, points) for (points, lastAscentSquare) in getPointsForClimbs(track) ]

def createSprintsObservers(track):
    return [ createSprintObserver(lastSquare, points) for (lastSquare, points) in getPointsForSprints(track) ]

from ridersFactory import createRider
from cards import fullRecovery
def sprinteurOnlyTeam(color):
    sprinteur = createRider(sprinteurSpecialist(), fullRecovery)
    return Team(color, [sprinteur])

class Displays:
    def __init__(self, window, layout, roadDisplay, onCardsDisplay):
        self.window = window
        self.roadDisplay = roadDisplay
        self.cardsDisplays = [CardsDisplay(frame, rider) for rider, frame in zip(onCardsDisplay, layout.getDecksFrames())]

    def update(self, riders, race):
        self.roadDisplay.endOfTurnUpdate()
        for display in self.cardsDisplays:
            display.displayCards(display.rider.cards.inDeck(), display.rider.cards.discard, display.rider.cards.played)
        self.window.update()


def main():
    args = parseArgs()
    if args.integration:
        return integrationTests()

    root = tk.Tk()
    root.title("flamme rouge")
    window = tk.Frame(root)
    window.grid()
    single = args.single

    if single:
        racesCount = 1
    else:
        racesCount = createSimpleMenu(window, range(1, 6))

    clock = 0.3
    if args.faster:
        clock /= args.faster

    if args.faster:
        ridersKind = [ rouleurSpecialist(), sprinteurSpecialist() ]
    else:
        ridersKind = pickRiders(window)
    teams = [ createBot("green") if args.faster else createHuman(root, "green", ridersKind) ]
    for color in ["blue", "red", "black"]:
        teams.append(createBot(color))
    tour = Tour(teams)
    tracks = [ randomPresetTrack() for i in range(racesCount) ]
    runner = Runner(window, clock, len(ridersKind))
    runner.runTour(tour, tracks)

    window.bind("<Escape>", lambda e: window.destroy())
    window.mainloop()


def pickRiders(window):
    number = createSimpleMenu(window, [1, 2, 3, 4])
    return [ createMenu(window, [ (rider.name, rider) for rider in [ rouleurSpecialist(), sprinteurSpecialist(), grimpeurSpecialist() ]]) for i in range(number) ]


def createDisplays(track, layout, clock, window, onCardsDisplay):
    roadDisplay = RoadDisplay(layout.getTrackFrame(), track)
    eventDisplay = EventDisplay(layout.getEventFrame())
    animation = Animation([EventAnimator(eventDisplay), RoadAnimator(roadDisplay, clock)], clock)
    displays = Displays(window, layout, roadDisplay, onCardsDisplay)
    return displays, animation

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

import argparse
def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--faster', type=int)
    parser.add_argument('--single', action="store_true")
    parser.add_argument('--integration', action="store_true")
    return parser.parse_args()

def createHuman(rootWindow, color, specialists):
    team = Team(color, [createHumanRider(kind) for kind in specialists])
    window = tk.Toplevel(rootWindow)
    player = createHumanPlayer(rootWindow, window, team)
    team.player = player
    return team

def createBot(color):
    team = Team(color, duo(createBotRider))
    player = createBotPlayer(team)
    team.player = player
    return team

def duo(create):
    return [create(rouleurSpecialist()), create(sprinteurSpecialist())]

def createHumanPlayer(rootWindow, choicesFrame, team):
    oracle = UserChoice(choicesFrame)
    def onExit(oracle, rootWindow):
        oracle.dontWait()
        rootWindow.destroy()
    rootWindow.protocol("WM_DELETE_WINDOW", partial(onExit, oracle, rootWindow))
    return Player(oracle, team.riders, [CardDecorator()])

def createBotPlayer(team):
    return Player(FirstOracle(), team.riders, [CardDecorator()])

class FirstOracle():
    def pick(self, any):
        return 0

if __name__ == "__main__":
    main()

