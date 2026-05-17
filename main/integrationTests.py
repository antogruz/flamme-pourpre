#!/usr/bin/env python3

import tkinter as tk
from runner import Runner
from jeu.tour import Tour
from jeu.tracks import randomPresetTrack
from teamBuilder import TeamBuilder
from propulsion import SimpleTeamPropulsion
from teamsDirector import TeamsDirector
from team import DefaultOracle
from ridersDirector import RidersDirector
from riderBuilderWithAppearance import RiderBuilderWithAppearance
from riderBuilderWithSpecialDisplay import RiderBuilderWithSpecialDisplay
from displayRegistry import DisplayRegistry
from beau.appearances import Appearances
from beau.frames import Frames

def integrationTests():
    window = tk.Tk()
    testDice(window)
    integrationSingle(window)
    twoRacesOpportunistic(window)
    window.mainloop()

def integrationSingle(window):
    runner = Runner(window, 0.003)
    appearances = Appearances()
    teamsDirector = TeamsDirector(appearances)
    teams = [teamsDirector.makeStandardBots(color) for color in ["green", "red", "blue", "black", "magenta"]]
    runner.runRace(randomPresetTrack(len(teams)), teams, appearances=appearances)

def testDice(window):
    runner = Runner(window, 0.003)
    appearances = Appearances()
    teamsDirector = TeamsDirector(appearances)
    teams = [teamsDirector.makeDiceBots(color) for color in ["blue", "red", "black"]]
    runner.runRace(randomPresetTrack(len(teams)), teams, appearances=appearances)

def twoRacesOpportunistic(window):
    appearances = Appearances()
    displayRegistry = DisplayRegistry()
    colors = ["blue", "red", "black"]
    layout = OpportunisticLayout(window, len(colors))
    teams = []
    oracle = DefaultOracle()
    for i, color in enumerate(colors):
        tb = TeamBuilder()
        tb.buildPropulsion(SimpleTeamPropulsion())
        riderDirector = RidersDirector(
            RiderBuilderWithSpecialDisplay(displayRegistry, appearances, layout.cards[i], layout.specials[i], layout.talents[i])
        )
        tb.addRider(riderDirector.makeOpportunistic(oracle, color))
        teams.append(tb.getResult())
    tour = Tour(teams)
    runner = Runner(window, 0.003, displayRegistry.getAll())
    runner.runTour(tour, [randomPresetTrack, randomPresetTrack], appearances)

class OpportunisticLayout:
    def __init__(self, root, ridersCount):
        window = tk.Toplevel(root)
        frames = Frames(window)
        self.cards = frames.newLine(ridersCount)
        self.specials = frames.newLine(ridersCount)
        self.talents = frames.newLine(ridersCount)

if __name__ == "__main__":
    integrationTests()

