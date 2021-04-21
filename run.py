#!/usr/bin/env python3

import tkinter as tk
from frames import Frames
from riderDisplay import addRouleurDisplay, addSprinteurDisplay, copyDisplay
from track import Track
from rider import Rider
from player import Player
from race import Race
from cards import Cards
import riderMove
import random
from display import RoadDisplay

def main():
    window = tk.Tk()
    window.title("flamme rouge")

    track = Track(createTrack())
    frames = Frames()
    players, riders = createRiders(frames.new(window))
    race = Race(track, riders, players)
    roadDisplay = RoadDisplay(frames.new(window), track, riders)
    for r in race.riders:
        animate(r, roadDisplay)

    window.update()
    while not race.isOver():
        race.newTurn()
        roadDisplay.update()
        roadDisplay.ranking(race.ranking())
        window.update()

    window.mainloop()

def createRiders(choicesFrame):
    players = []
    riders = []
    square = 0
    oracle = PlayerChoice(choicesFrame)
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

from animation import AnimatedRider
def animate(rider, display):
    rider.riderMove = AnimatedRider(rider.riderMove, display)
    copyDisplay(rider.riderMove, rider)

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


main()



