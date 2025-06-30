#!/usr/bin/env python3

import tkinter as tk
from runner import Runner
from tour import Team, Tour
from tracks import *
from frames import clear
from jeu.tracks import randomPresetTrack
from teamBuilder import TeamBuilder
from riderBuilder import RiderBuilder
from decorators.riderDisplay import sprinteurShade, rouleurShade, grimpeurShade, opportunisticShade
from riderMove import MovementRules
from propulsion import SequentialPropulsion, SimpleTeamPropulsion
from teamsDirector import TeamsDirector, FirstOracle

def integrationTests():
    window = tk.Tk()
    runner = Runner(window, 0.003)
    testDice(runner)
    integrationSingle(runner)
    twoRacesOpportunistic(runner)
    window.mainloop()

def integrationSingle(runner):
    teams = []
    for color in ["green", "red", "blue", "black", "magenta"]:
        tb = TeamBuilder()
        tb.buildColor(color)
        tb.buildPropulsion(SimpleTeamPropulsion())
        rb = RiderBuilder()
        rb.buildTexts(sprinteurShade, "Sprinteur")
        rb.buildDice([2, 3, 4, 5, 6, 9])
        rb.buildMovementRules(MovementRules())
        tb.addRider(rb.getResult())
        rb = RiderBuilder()
        rb.buildTexts(rouleurShade, "Rouleur")
        rb.buildDice([3, 4, 5, 6, 7, 8])
        rb.buildMovementRules(MovementRules())
        tb.addRider(rb.getResult())
        teams.append(tb.getResult())
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
        rb = RiderBuilder()
        rb.buildMovementRules(MovementRules())
        rb.buildTexts(opportunisticShade, "Opportunistic")
        rb.buildOracle(oracle)
        rb.buildOpportunisticDeck([2, 3, 4, 5, 9])
        tb.addRider(rb.getResult())
        team = tb.getResult()
        teams.append(team)
    tour = Tour(teams)
    runner.runTour(tour, [randomPresetTrack, randomPresetTrack])

if __name__ == "__main__":
    integrationTests()

