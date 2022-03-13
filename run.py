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


def main():
    window = tk.Tk()
    window.title("flamme rouge")

    faster = parseArgs().faster
    track = colDuBallon() if faster else pickTrack(window)
    layout = RaceLayout(window, 2)
    players, riders = createRiders(layout.getUserFrame(), faster)
    onCardsDisplay = riders[0:2]
    clock = 0.3
    if faster:
        clock /= faster
    roadDisplay = RoadDisplay(layout.getTrackFrame(), track)
    roadDisplay.displayRiders(riders)
    animation = Animation(roadDisplay, clock)

    race = Race(track, riders, players)

    window.update()
    #tour = Tour()
    while not race.isOver():
        for rider, frame in zip(onCardsDisplay, layout.getDecksFrames()):
            displayRiderCards(frame, rider)
        logger = Logger()
        race.newTurn(logger)
        animation.animate(logger.getMoves(), logger.getGroups(), logger.getExhausted())
        roadDisplay.displayRiders(race.riders)
        roadDisplay.ranking(race.ranking())
        #tour.checkNewArrivals(race.ranking())
        window.update()

    #tour.endRace(race.ranking())
    #tour.scores()
    #tour.times()

    window.bind("<Escape>", lambda e: window.destroy())
    window.mainloop()

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

from rider import Rider
def createRiders(choicesFrame, fast):
    players = []
    riders = []
    square = 0
    if fast:
        oracle = FirstOracle()
    else:
        oracle = PlayerChoice(choicesFrame)

    for color in ["green", "red", "blue", "black"]:
        player, group = createPlayer(color, oracle, square)
        oracle = FirstOracle()
        square += 1
        players.append(player)
        riders += group
    return players, riders

def createPlayer(color, oracle, square):
        rouleur = createRider(color, square, 0, createRouleur())
        sprinteur = createRider(color, square, 1, createSprinteur())
        return Player(oracle, [rouleur, sprinteur]), [rouleur, sprinteur]

class Specialist:
    def __init__(self, name, deck, shade):
        self.name = name
        self.deck = deck
        self.shade = shade

def createRider(color, square, lane, specialist):
    rider = Rider(specialist.name, Cards(specialist.deck, random.shuffle), riderMove.Rider(square, lane))
    rider.shade = specialist.shade
    rider.color = color
    return rider

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
    deck = []
    for i in range(3):
        deck += [3, 4, 5, 6, 7]
    return deck

def sprinteurDeck():
    deck = []
    for i in range(3):
        deck += [2, 3, 4, 5, 9]
    return deck

main()

