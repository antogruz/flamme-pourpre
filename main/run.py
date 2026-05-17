#!/usr/bin/env python3

import tkinter as tk
from jeu.tracks import randomPresetTrack
from beau.menu import *
from beau.frames import Frames
from runner import Runner
from jeu.tour import Tour
from jeu.teamBuilder import TeamBuilder
from ridersDirector import RidersDirector
from riderBuilderWithSpecialDisplay import RiderBuilderWithSpecialDisplay
from displayRegistry import DisplayRegistry
from teamsDirector import TeamsDirector
from jeu.propulsion import SequentialPropulsion
from beau.appearances import Appearances
from specialTour.teamProgression import TalentTeamProgression
from functools import partial

def main():
    root = tk.Tk()
    root.title("flamme rouge")
    window = tk.Frame(root)
    window.grid()
    clock = 0.3

    gameMode = createSimpleMenu(window, ["Tour", "Special Tour"], "Game mode")
    racesCount = createSimpleMenu(window, range(1, 6), "How many races to play?")
    ridersCount = createSimpleMenu(window, [1, 2, 3, 4], "How many riders in your team?")
    playerLayout = PlayerLayout(newWindow(root), ridersCount)
    appearances = Appearances()
    oracle = createPlayerOracle(root, playerLayout.choices, appearances)
    teamColor = "green"
    tb = TeamBuilder()
    tb.buildOracle(oracle)
    tb.buildPropulsion(SequentialPropulsion(oracle))

    displayRegistry = DisplayRegistry()
    for i in range(ridersCount):
        riderType = createSimpleMenu(window, ["Rouleur", "Sprinteur", "Grimpeur", "Opportunistic"], "Add a rider to your team")

        director = RidersDirector(RiderBuilderWithSpecialDisplay(displayRegistry, appearances, playerLayout.ridersCards[i], playerLayout.ridersSpecialFrames[i]))

        if riderType == "Rouleur":
            rider = director.makeRouleur(oracle, teamColor)
        elif riderType == "Sprinteur":
            rider = director.makeSprinteur(oracle, teamColor)
        elif riderType == "Grimpeur":
            rider = director.makeGrimpeur(oracle, teamColor)
        elif riderType == "Opportunistic":
            rider = director.makeOpportunistic(oracle, teamColor)

        tb.addRider(rider)

    if gameMode == "Special Tour":
        tb.buildProgression(TalentTeamProgression(tb.riders, oracle))
    humanTeam = tb.getResult()
    teamsDirector = TeamsDirector(appearances)
    botTeams = []
    botsFactory = createMenu(window, [("Standard", teamsDirector.makeStandardBots), ("Dice", teamsDirector.makeDiceBots), ("Muscle", teamsDirector.makeMuscleTeam)], "Choose the type of bots")
    for color in ["blue", "red", "black"]:
        botTeams.append(botsFactory(color))

    tour = Tour([humanTeam] + botTeams)
    tracks = [ randomPresetTrack for i in range(racesCount) ]

    allDisplays = displayRegistry.getAll()
    runner = Runner(window, clock, allDisplays)
    bonusPerRace = 4 if gameMode == "Special Tour" else 0
    runner.runTour(tour, tracks, appearances, bonusPerRace)

    window.bind("<Escape>", lambda e: window.destroy())
    window.mainloop()

def newWindow(frame):
    return tk.Toplevel(frame)

class PlayerLayout:
    def __init__(self, window, ridersCount):
        frames = Frames(window)
        self.choices = frames.new()
        self.ridersCards = frames.newLine(ridersCount)
        self.ridersSpecialFrames = frames.newLine(ridersCount)

def createPlayerOracle(root, window, appearances):
    oracle = UserChoice(window, appearances)
    def onExit(oracle):
        oracle.dontWait()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", partial(onExit, oracle))
    return oracle

if __name__ == "__main__":
    main()

