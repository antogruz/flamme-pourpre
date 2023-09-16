#!/usr/bin/env python3

import tkinter as tk
from run import Runner, createBotPlayer, createBot
from tour import Team, Tour
from tracks import *
from frames import clear

def integrationTests():
    window = tk.Tk()
    runner = Runner(window, 0.003, 0)
    twoRacesSprinteursOnly(runner)
    clear(window)
    integrationSingle(runner)
    window.mainloop()


def integrationTests():
    window = tk.Tk()
    runner = Runner(window, 0.003, 0)
    twoRacesSprinteursOnly(runner)
    clear(window)
    integrationSingle(runner)
    window.mainloop()

def integrationSingle(runner):
    teams = [ createBot(color) for color in ["green", "red", "blue", "black", "magenta"] ]
    runner.runRace(colDuBallon(), teams)

def twoRacesSprinteursOnly(runner):
    teams = [ sprinteurOnlyTeam(color) for color in ["blue", "red", "black"] ]
    for team in teams:
        team.player = createBotPlayer(team)
    tour = Tour(teams)
    runner.runTour(tour, [corsoPaseo(), firenzeMilano()])

from cards import fullRecovery
from ridersFactory import *
def sprinteurOnlyTeam(color):
    sprinteur = createRider(sprinteurSpecialist(), fullRecovery)
    return Team(color, [sprinteur])

if __name__ == "__main__":
    integrationTests()

