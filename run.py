#!/usr/bin/env python3

import tkinter as tk
from riderDisplay import *
from track import Track
from tracks import *
from player import Player
from race import Race
from cards import Cards
import riderMove
import random
from display import RoadDisplay
from animation import Logger, Animation
from raceLayout import RaceLayout
from cardsDisplay import displayCards
from menu import *
from tour import Tour, Team


def main():
    window = tk.Tk()
    window.title("flamme rouge")

    teams = createTeams()
    tour = Tour(teams)

    for i in range(1):
        tour.newRace()
        playRace(window, tour)

    print(tour.scores())
    print(tour.times())

    window.bind("<Escape>", lambda e: window.destroy())
    window.mainloop()

def playRace(window, tour):
    faster = parseArgs().faster
    track = colDuBallon() if faster else pickTrack(window)
    layout = RaceLayout(window, 2)
    players = createPlayers(tour.teams, layout.getUserFrame(), faster)

    riders = tour.getRiders()
    onCardsDisplay = riders[0:2]
    clock = 0.3
    if faster:
        clock /= faster
    roadDisplay = RoadDisplay(layout.getTrackFrame(), track)
    setRidersOnStart(riders)
    roadDisplay.displayRiders(riders)
    animation = Animation(roadDisplay, clock)

    race = Race(track, riders, players)

    window.update()

    while not race.isOver():
        for rider, frame in zip(onCardsDisplay, layout.getDecksFrames()):
            displayRiderCards(frame, rider)
        logger = Logger()
        race.newTurn(logger)
        animation.animate(logger.getMoves(), logger.getGroups(), logger.getExhausted())
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
    return parser.parse_args()

def createTeams():
    return [ Team(color, [createRider(createRouleur()), createRider(createSprinteur())])
            for color in ["green", "red", "blue", "black"] ]


def createRider(specialist):
    rider = Rider(specialist.name, Cards(specialist.deck, random.shuffle))
    rider.shade = specialist.shade
    return rider

from rider import Rider
def createPlayers(teams, choicesFrame, fast):
    players = []
    if fast:
        oracle = FirstOracle()
    else:
        oracle = PlayerChoice(choicesFrame)

    for team in teams:
        player = Player(oracle, team.riders)
        oracle = FirstOracle()
        players.append(player)
    return players


class Specialist:
    def __init__(self, name, deck, shade):
        self.name = name
        self.deck = deck
        self.shade = shade

def createRouleur():
    return Specialist("Rouleur", rouleurDeck(), rouleurShade)

def createSprinteur():
    return Specialist("Sprinteur", sprinteurDeck(), sprinteurShade)


def animate(rider, display):
    rider.display = display

class FirstOracle():
    def pick(self, any):
        return 0

def rouleurDeck():
    return threeTimes([3, 4, 5, 6, 7])

def sprinteurDeck():
    return threeTimes([2, 3, 4, 5, 9])

def threeTimes(five):
    return [ card for card in five for i in range(3) ]
main()

