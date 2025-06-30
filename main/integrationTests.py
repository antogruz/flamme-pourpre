#!/usr/bin/env python3

import tkinter as tk
from runner import Runner
from jeu.tour import Tour
from jeu.tracks import randomPresetTrack
from teamBuilder import TeamBuilder
from propulsion import SimpleTeamPropulsion
from teamsDirector import TeamsDirector, FirstOracle
from ridersDirector import RidersDirector

def integrationTests():
    window = tk.Tk()
    runner = Runner(window, 0.003)
    testDice(runner)
    integrationSingle(runner)
    twoRacesOpportunistic(runner)
    window.mainloop()

def integrationSingle(runner):
    teams = []
    teamsDirector = TeamsDirector()
    for color in ["green", "red", "blue", "black", "magenta"]:
        teams.append(teamsDirector.makeStandardBots(color))
    runner.runRace(randomPresetTrack(len(teams)), teams)

def testDice(runner):
    teamsDirector = TeamsDirector()
    teams = [teamsDirector.makeDiceBots(color) for color in ["blue", "red", "black"]]
    runner.runRace(randomPresetTrack(len(teams)), teams)

def twoRacesOpportunistic(runner):
    teams = []
    oracle = FirstOracle()
    for color in ["blue", "red", "black"]:
        tb = TeamBuilder()
        tb.buildColor(color)
        tb.buildPropulsion(SimpleTeamPropulsion())
        riderDirector = RidersDirector()
        tb.addRider(riderDirector.makeOpportunistic(oracle))
        team = tb.getResult()
        teams.append(team)
    tour = Tour(teams)
    runner.runTour(tour, [randomPresetTrack, randomPresetTrack])

if __name__ == "__main__":
    integrationTests()

