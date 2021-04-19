#!/usr/bin/env python3

import tkinter as tk
from trackDisplay import displayTrack, empty
from frames import Frames
from riderDisplay import addRouleurDisplay, addSprinteurDisplay, displayRider, displayRiderAtPosition, copyDisplay
from track import Track
from obstacles import Obstacles
from rider import Rider
from player import Player
from race import Race
from cards import Cards
import riderMove
import random
from display import displayBoard, displayRiders, displayRanking

def main():
    window = tk.Tk()
    window.title("flamme rouge")

    track = Track(createTrack())
    frames = Frames()
    players, riders = createRiders(frames.new(window))
    race = Race(track, riders, players)
    boardWidgets = displayBoard(frames.new(window), track, riders)
    for r in race.riders:
        animate(r, boardWidgets, window)

    window.update()
    while not race.isOver():
        race.newTurn()
        updateDisplay(boardWidgets, race.riders)
        displayRanking(boardWidgets, race.ranking())
        window.update()

    window.mainloop()

def createRiders(frame):
    players = []
    riders = []
    square = 0
    oracle = PlayerChoice(frame)
    for color in ["green", "red", "blue", "black"]:
        player, group = createPlayer(color, oracle, square)
        oracle = FirstOracle()
        square += 1
        players.append(player)
        riders += group
    return players, riders

def createPlayer(color, oracle, square):
        rouleur = createRouleur(color, square, 0)
        sprinteur = createSprinteur(color, square, 1)
        return Player(oracle, [rouleur, sprinteur]), [rouleur, sprinteur]

def createRouleur(color, square, lane):
    rider = Rider("Rouleur", Cards(rouleurDeck(), random.shuffle), riderMove.Rider(square, lane))
    addRouleurDisplay(rider, color)
    return rider

def createSprinteur(color, square, lane):
    rider = Rider("Sprinteur", Cards(sprinteurDeck(), random.shuffle), riderMove.Rider(square, lane))
    addSprinteurDisplay(rider, color)
    return rider

def animate(rider, roadWidgets, frame):
    rider.riderMove = AnimatedRider(rider.riderMove, roadWidgets, frame)
    copyDisplay(rider.riderMove, rider)

from time import sleep
class AnimatedRider():
    def __init__(self, riderMove, roadWidgets, frame):
        self.riderMove = riderMove
        self.roadWidgets = roadWidgets
        self.frame = frame

    def position(self):
        return self.riderMove.position()

    def getSquare(self):
        return self.riderMove.getSquare()

    def move(self, distance, track, obstacles):
        saved = self.position()
        self.riderMove.move(distance, track, obstacles)
        self.animate(obstacles, saved, self.position())

    def getSlipstream(self, track):
        return self.riderMove.getSlipstream(track)

    def animate(self, obstacles, start, end):
        sleep(0.3)
        if start[0] == end[0]:
            return

        empty(self.roadWidgets[start[0]][start[1]])
        next = findNextEmpty(start, end, obstacles)
        displayRiderAtPosition(self.roadWidgets, self, next)
        self.frame.update()
        self.animate(obstacles, next, end)

def findNextEmpty(start, end, obstacles):
    nextSquare = start[0] + 1
    if nextSquare == end[0]:
        return end

    for lane in range(2):
        if obstacles.isFree((nextSquare, lane)):
            return (nextSquare, lane)

    return (nextSquare, 2)


class FirstOracle():
    def pick(self, any):
        return 0

from functools import partial
class PlayerChoice():
    def __init__(self, frame):
        self.frame = frame

    def pick(self, choices):
        answer = tk.IntVar()
        def setChoice(n):
            answer.set(n)

        for i, choice in enumerate(choices):
            tk.Button(self.frame, text = choice, command = partial(setChoice, i)).pack(side = "left")

        self.frame.update()
        self.frame.wait_variable(answer)

        clear(self.frame)
        return answer.get()

def clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()

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

def updateDisplay(boardWidgets, riders):
    removeTokens(boardWidgets)
    displayRiders(boardWidgets, riders)

def removeTokens(boardWidgets):
    for square in boardWidgets:
        for lane in square:
            empty(lane)


main()



