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
    teams = [ createBot(color) for color in ["green", "red", "blue", "black", "magenta"] ]
    track = colDuBallon()
    singleRace(window, track, teams, 0.003, 6)

def allRiders(teams):
    return [rider for team in teams for rider in team.riders]

def allPlayers(teams):
    return [team.player for team in teams]

def noLog(ranking):
    pass

def singleRace(window, track, teams, clock, decksDisplayed = 2, logRanking = noLog):
    for team in teams:
        team.player.resetRiders(team.riders)
    riders = allRiders(teams)
    players = allPlayers(teams)
    for rider in riders:
        rider.cards.newRace()

    layout = RaceLayout(window, decksCount = decksDisplayed)
    displays, animation = createDisplays(track, layout, clock, window, riders[0:decksDisplayed])
    setRidersOnStart(riders)
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
    for team in teams:
        team.player = Player(FirstOracle(), team.riders)
    tour = Tour(teams)
    for track in [corsoPaseo(), firenzeMilano()]:
        tour.newRace()
        singleRace(window, track, tour.teams, 0.003, 3, tour.checkNewArrivals)
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

    teams = [ createBot("green") if args.faster else createHuman(root, "green") ]
    for color in ["blue", "red", "black"]:
        teams.append(createBot(color))
    tour = Tour(teams)

    for i in range(racesCount):
        tour.newRace()
        track = randomPresetTrack()
        singleRace(window, track, tour.teams, clock, 2, tour.checkNewArrivals)
        clear(window)
        frames = Frames(window)
        displayResults(frames.new(), tour.scores(), tour.times())
        createSimpleMenu(frames.new(), ["Next Race!"])
        clear(window)

    window.bind("<Escape>", lambda e: window.destroy())
    window.mainloop()


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

def createHuman(rootWindow, color):
    team = Team(color, duo(createHumanRider))
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
    return Player(oracle, team.riders)

def createBotPlayer(team):
    return Player(FirstOracle(), team.riders)

class FirstOracle():
    def pick(self, any):
        return 0

if __name__ == "__main__":
    main()

