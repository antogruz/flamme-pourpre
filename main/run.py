#!/usr/bin/env python3

import tkinter as tk
from tracks import *
from player import Player
import factory
from menu import *
from ridersFactory import *
from runner import Runner
from tour import Tour
from cardsDisplay import CardsDisplay

def main():
    root = tk.Tk()
    root.title("flamme rouge")
    window = tk.Frame(root)
    window.grid()

    racesCount = createSimpleMenu(window, range(1, 6), "How many races to play?")

    clock = 0.3
    ridersKind = pickRiders(window)
    playerLayout = PlayerLayout(newWindow(root), len(ridersKind))
    humanFactory = factory.Human(root, playerLayout.choices)
    teams = [ humanFactory.createTeam("green", ridersKind) ] + [factory.Bot().createTeam(color) for color in ["blue", "red", "black"]]
    humanRiders = teams[0].riders
    cardsDisplayers = [ CardsDisplay(riderFrame, rider) for rider, riderFrame in zip(humanRiders, playerLayout.ridersCards) ]
    specialDisplayers = humanFactory.createSpecialDisplays(ridersKind, playerLayout.ridersSpecialFrames)
    tour = Tour(teams)
    tracks = [ randomPresetTrack() for i in range(racesCount) ]
    runner = Runner(window, clock, cardsDisplayers + specialDisplayers)
    runner.runTour(tour, tracks)

    window.bind("<Escape>", lambda e: window.destroy())
    window.mainloop()

def newWindow(frame):
    return tk.Toplevel(frame)

class PlayerLayout:
    def __init__(self, window, ridersCount):
        factory = Frames(window)
        self.choices = factory.new()
        self.ridersCards = factory.newLine(ridersCount)
        self.ridersSpecialFrames = factory.newLine(ridersCount)


def pickRiders(window):
    number = createSimpleMenu(window, [1, 2, 3, 4], "How many riders in your team?")
    return [ createMenu(window, [ (rider.name, rider) for rider in [ rouleurSpecialist(), sprinteurSpecialist(), grimpeurSpecialist(), opportunisticSpecialist() ]], "Add a rider to your team") for i in range(number) ]


if __name__ == "__main__":
    main()

