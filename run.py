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
from animation import Logger, Animation, EventAnimator, RoadAnimator
from raceLayout import RaceLayout
from cardsDisplay import CardsDisplay
from menu import *
from tour import Tour, Team
from ridersFactory import createHumanRider, createBotRider, rouleurSpecialist, sprinteurSpecialist
from eventDisplay import EventDisplay
from results import displayResults
from frames import Frames

def integrationTests():
    window = tk.Tk()
    integrationSingle(window)
    clear(window)
    twoRacesSprinteursOnly(window)
    window.mainloop()

def integrationSingle(window):
    teamsColors = [(["green", "red", "blue", "black", "magenta"], createBotRider)]
    teams = createTeamsByGroups(teamsColors)
    players = [ Player(FirstOracle(), team.riders) for team in teams ]
    track = colDuBallon()
    riders = allRiders(teams)
    singleRace(window, track, riders, players, 0.003)

def allRiders(teams):
    return [rider for team in teams for rider in team.riders]

def noLog(ranking):
    pass

def singleRace(window, track, riders, players, clock, logRanking = noLog):
    decksDisplayed = 4
    layout = RaceLayout(window, decksCount = decksDisplayed)
    setRidersOnStart(riders)
    displays, animation = createDisplays(track, layout, clock, window, riders[0:decksDisplayed])
    race = Race(track, riders, players)
    displays.update(riders, race)

    while not race.isOver():
        logger = Logger()
        race.newTurn(logger)
        animation.animate(logger.getMoves(), logger.getGroups(), logger.getExhausted())
        logRanking(race.ranking())
        displays.update(riders, race)

def twoRacesSprinteursOnly(window):
    teams = [ sprinteurOnlyTeam(color) for color in ["blue", "red", "black"] ]
    tour = Tour(teams)
    for track in [corsoPaseo(), firenzeMilano()]:
        players = [ Player(FirstOracle(), team.riders) for team in teams ]
        tour.newRace()
        for rider in tour.getRiders():
            rider.cards.newRace()
        singleRace(window, track, tour.getRiders(), players, 0.003, tour.checkNewArrivals)
        clear(window)
        frames = Frames(window)
        displayResults(frames.new(), tour.scores(), tour.times())
        createSimpleMenu(frames.new(), ["Next Race!"])
        clear(window)


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
        self.roadDisplay.displayRiders(riders)
        self.roadDisplay.ranking(race.ranking())
        for display in self.cardsDisplays:
            display.displayCards(display.rider.cards.inDeck(), display.rider.cards.discard, display.rider.cards.played)
        self.window.update()


def main():
    args = parseArgs()
    if args.integration:
        return integrationTests()

    window = tk.Tk()
    window.title("flamme rouge")
    single = args.single

    if single:
        racesCount = 1
    else:
        racesCount = createSimpleMenu(window, range(1, 6))

    teams = createTeams()
    tour = Tour(teams)

    for i in range(racesCount):
        tour.newRace()
        for rider in tour.getRiders():
            rider.cards.newRace()
        playRace(window, tour)
        clear(window)
        frames = Frames(window)
        displayResults(frames.new(), tour.scores(), tour.times())
        createSimpleMenu(frames.new(), ["Next Race!"])
        clear(window)

    window.bind("<Escape>", lambda e: window.destroy())
    window.mainloop()


def playRace(window, tour):
    faster = parseArgs().faster
    track = colDuBallon() if faster else pickTrack(window)
    layout = RaceLayout(window, decksCount=2)
    players = createPlayers(window, tour.teams, layout.getUserFrame(), faster)

    riders = tour.getRiders()
    onCardsDisplay = riders[0:2]
    clock = 0.3
    if faster:
        clock /= faster
    displays, animation = createDisplays(track, layout, clock, window, onCardsDisplay)
    setRidersOnStart(riders)

    race = Race(track, riders, players)
    displays.update(riders, race)

    while not race.isOver():
        logger = Logger()
        race.newTurn(logger)
        animation.animate(logger.getMoves(), logger.getGroups(), logger.getExhausted())
        tour.checkNewArrivals(race.ranking())
        displays.update(riders, race)

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

def createTeams():
    groups = []
    groups.append((["green"], createHumanRider))
    groups.append((["red", "blue", "black"], createBotRider))
    return createTeamsByGroups(groups)


def createTeamsByGroups(groups):
    teams = []
    for colors, create in groups:
        teams += [Team(color, duo(create)) for color in colors]
    return teams

def duo(create):
    return [create(rouleurSpecialist()), create(sprinteurSpecialist())]

from rider import Rider
def createPlayers(rootWindow, teams, choicesFrame, fast):
    players = []
    if fast:
        oracle = FirstOracle()
    else:
        oracle = UserChoice(choicesFrame)
        def onExit(oracle, rootWindow):
            oracle.dontWait()
            rootWindow.destroy()
        rootWindow.protocol("WM_DELETE_WINDOW", partial(onExit, oracle, rootWindow))

    for team in teams:
        player = Player(oracle, team.riders)
        oracle = FirstOracle()
        players.append(player)
    return players


class FirstOracle():
    def pick(self, any):
        return 0

if __name__ == "__main__":
    main()

