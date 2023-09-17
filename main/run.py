#!/usr/bin/env python3

import tkinter as tk
from tracks import *
from player import Player
from animation import CardDecorator
import factory
from menu import *
from ridersFactory import *
from runner import Runner
from tour import Tour

def main():
    root = tk.Tk()
    root.title("flamme rouge")
    window = tk.Frame(root)
    window.grid()

    racesCount = createSimpleMenu(window, range(1, 6), "How many races to play?")

    clock = 0.3
    ridersKind = pickRiders(window)
    teams = [ factory.Human(root).createTeam("green", ridersKind) ] + [factory.Bot().createTeam(color) for color in ["blue", "red", "black"]]
    tour = Tour(teams)
    tracks = [ randomPresetTrack() for i in range(racesCount) ]
    runner = Runner(window, clock, len(ridersKind))
    runner.runTour(tour, tracks)

    window.bind("<Escape>", lambda e: window.destroy())
    window.mainloop()


def pickRiders(window):
    number = createSimpleMenu(window, [1, 2, 3, 4], "How many riders in your team?")
    return [ createMenu(window, [ (rider.name, rider) for rider in [ rouleurSpecialist(), sprinteurSpecialist(), grimpeurSpecialist() ]], "Add a rider to your team") for i in range(number) ]


if __name__ == "__main__":
    main()

