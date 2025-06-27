#!/usr/bin/env python3

import tkinter as tk
from runner import Runner
from factory import *
from tour import Team, Tour
from tracks import *
from frames import clear
from jeu.tracks import randomPresetTrack

def integrationTests():
    window = tk.Tk()
    runner = Runner(window, 0.003)
    twoRacesSprinteursOnly(runner)
    clear(window)
    integrationSingle(runner)
    window.mainloop()

def integrationSingle(runner):
    teams = createTeams(Bot(), ["green", "red", "blue", "black", "magenta"])
    runner.runRace(randomPresetTrack(5), teams)

def twoRacesSprinteursOnly(runner):
    teams = createTeams(Bot(), ["blue", "red", "black"], [opportunisticSpecialist()])
    tour = Tour(teams)
    runner.runTour(tour, [randomPresetTrack, randomPresetTrack])

def createTeams(factory, colors, kinds = classicDuo()):
    return [ factory.createTeam(color, kinds) for color in colors ]


if __name__ == "__main__":
    integrationTests()

