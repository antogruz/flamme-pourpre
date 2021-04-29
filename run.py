#!/usr/bin/env python3

import tkinter as tk
from frames import Frames
from riderDisplay import *
from track import Track
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
    frames = Frames(window)
    faster = parseArgs().faster
    players, riders = createRiders(frames.new(), faster)
    clock = 0.3
    if faster:
        clock /= faster
    roadDisplay = RoadDisplay(frames.new(), track, riders, clock)
    race = Race(track, riders, players, roadDisplay)
    for r in race.riders:
        animate(r, roadDisplay)

    window.update()
    while not race.isOver():
        race.newTurn()
        roadDisplay.update()
        roadDisplay.ranking(race.ranking())
        window.update()

    window.mainloop()

import argparse
def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--faster', type=int)
    return parser.parse_args()

from moveAnimation import AnimatedRider
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
    rider = AnimatedRider(specialist.name, Cards(specialist.deck, random.shuffle), riderMove.Rider(square, lane), None)
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



