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
from cardsDisplay import displayCards
from menu import *
from tour import Tour, Team
from ridersFactory import createHumanRider, createBotRider, rouleurSpecialist, sprinteurSpecialist
from eventDisplay import EventDisplay
from results import displayResults
from frames import Frames


def main():
    window = tk.Tk()
    window.title("flamme rouge")
    single = parseArgs().single

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
    players = createPlayers(tour.teams, layout.getUserFrame(), faster)

    riders = tour.getRiders()
    onCardsDisplay = riders[0:2]
    clock = 0.3
    if faster:
        clock /= faster
    roadDisplay = RoadDisplay(layout.getTrackFrame(), track)
    eventDisplay = EventDisplay(layout.getEventFrame())
    setRidersOnStart(riders)
    roadDisplay.displayRiders(riders)
    animation = Animation([EventAnimator(eventDisplay), RoadAnimator(roadDisplay, clock)], clock)

    race = Race(track, riders, players)

    window.update()

    while not race.isOver():
        for rider, frame in zip(onCardsDisplay, layout.getDecksFrames()):
            displayRiderCards(frame, rider)
        logger = Logger()
        race.newTurn(logger)
        animation.animate(logger.getMoves(), logger.getGroups(), logger.getExhausted())
        roadDisplay.displayRiders(riders)
        roadDisplay.ranking(race.ranking())
        tour.checkNewArrivals(race.ranking())
        window.update()

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


def displayRiderCards(frame, rider):
    displayCards(frame, rider, rider.cards.inDeck(), rider.cards.discard, rider.cards.played)

import argparse
def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--faster', type=int)
    parser.add_argument('--single', action="store_true")
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
def createPlayers(teams, choicesFrame, fast):
    players = []
    if fast:
        oracle = FirstOracle()
    else:
        oracle = UserChoice(choicesFrame)

    for team in teams:
        player = Player(oracle, team.riders)
        oracle = FirstOracle()
        players.append(player)
    return players


class FirstOracle():
    def pick(self, any):
        return 0

main()

