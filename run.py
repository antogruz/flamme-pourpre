#!/usr/bin/env python3

import tkinter as tk
from trackDisplay import displayTrack, empty
from frames import Frames
from riderDisplay import addRouleurDisplay, addSprinteurDisplay, displayRider
from track import Track
from obstacles import Obstacles
from rider import Rider
from player import Player
from game import Game
from cards import Cards
import riderMove
import random

def main():
    window = tk.Tk()
    window.title("flamme rouge")

    track = Track(createTrack())
    players, riders = createRiders()
    game = Game(track, riders, players)
    frames = Frames()
    boardWidgets = displayBoard(frames.new(window), track, riders)
    #choicesButtons(boardWidgets, frames.new(window), track, riders)
    nextTurnButton(boardWidgets, frames.new(window), game)
    window.mainloop()

def createRiders():
    players = []
    riders = []
    square = 0
    for color in ["green", "red", "blue", "black"]:
        rouleur = createRouleur(color, square, 0)
        sprinteur = createSprinteur(color, square, 1)
        player = Player(FirstOracle(), [rouleur, sprinteur])
        square += 1
        players.append(player)
        riders += [rouleur, sprinteur]
    return players, riders

def createRouleur(color, square, lane):
    rider = Rider("Rouleur", Cards(rouleurDeck(), random.shuffle), riderMove.Rider(square, lane))
    addRouleurDisplay(rider, color)
    return rider

def createSprinteur(color, square, lane):
    rider = Rider("Sprinteur", Cards(sprinteurDeck(), random.shuffle), riderMove.Rider(square, lane))
    addSprinteurDisplay(rider, color)
    return rider

class FirstOracle():
    def pick(self, any):
        return 0

def createTrack():
    return [(5, "start"), (8, "normal"), (6, "ascent"), (4, "descent"), (32, "normal"), (5, "end")]

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

def displayBoard(window, road, riders):
    trackWidgets = displayTrack(window, road)
    displayRiders(trackWidgets, riders)
    return trackWidgets


def choicesButtons(boardWidgets, window, road, riders):
    obstacles = Obstacles(riders)

    def forward(n):
        rider = riders[2]
        rider.move(n, road, obstacles)
        updateDisplay(boardWidgets, riders)

    def plus1():
        forward(1)
    def plus2():
        forward(2)
    def plus5():
        forward(5)
    def plus9():
        forward(9)

    for i, plus in zip([1, 2, 5, 9], [plus1, plus2, plus5, plus9]):
        tk.Button(window, text = i, command = plus).pack(side = "left")

def nextTurnButton(boardWidgets, window, game):
    def go():
        game.newTurn()
        updateDisplay(boardWidgets, game.riders)

    tk.Button(window, text = "New turn", command = go).pack(side = "left")


def updateDisplay(boardWidgets, riders):
    removeTokens(boardWidgets)
    displayRiders(boardWidgets, riders)


def removeTokens(boardWidgets):
    for square in boardWidgets:
        for lane in square:
            empty(lane)


def displayRiders(boardWidgets, riders):
    for rider in riders:
        displayRider(boardWidgets, rider)

main()



