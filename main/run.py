#!/usr/bin/env python3

import tkinter as tk
from jeu.tracks import randomPresetTrack
from beau.menu import *
from beau.frames import Frames
from runner import Runner
from jeu.tour import Tour
from beau.cardsDisplay import CardsDisplay
from jeu.teamBuilder import TeamBuilder
from ridersDirector import RidersDirector
from riderBuilderWithDisplay import RiderBuilderWithDisplay
from displayRegistry import DisplayRegistry
from teamsDirector import TeamsDirector, FirstOracle
from beau.opportunisticDisplay import OpportunisticDisplay
from jeu.propulsion import SequentialPropulsion
from functools import partial

def main():
    root = tk.Tk()
    root.title("flamme rouge")
    window = tk.Frame(root)
    window.grid()
    clock = 0.3

    racesCount = createSimpleMenu(window, range(1, 6), "How many races to play?")
    ridersCount = createSimpleMenu(window, [1, 2, 3, 4], "How many riders in your team?")
    playerLayout = PlayerLayout(newWindow(root), ridersCount)
    oracle = createPlayerOracle(root, playerLayout.choices)
    tb = TeamBuilder()
    tb.buildColor("green")
    tb.buildOracle(oracle)
    tb.buildPropulsion(SequentialPropulsion(oracle))

    displayRegistry = DisplayRegistry()
    for i in range(ridersCount):
        riderType = createSimpleMenu(window, ["Rouleur", "Sprinteur", "Grimpeur", "Opportunistic"], "Add a rider to your team")

        director = RidersDirector(RiderBuilderWithDisplay(displayRegistry, playerLayout.ridersCards[i], playerLayout.ridersSpecialFrames[i]))

        if riderType == "Rouleur":
            rider = director.makeRouleur(oracle)
        elif riderType == "Sprinteur":
            rider = director.makeSprinteur(oracle)
        elif riderType == "Grimpeur":
            rider = director.makeGrimpeur(oracle)
        elif riderType == "Opportunistic":
            rider = director.makeOpportunistic(oracle)

        tb.addRider(rider)

    humanTeam = tb.getResult()
    teamsDirector = TeamsDirector()
    botTeams = []
    botsFactory = createMenu(window, [("Standard", teamsDirector.makeStandardBots), ("Dice", teamsDirector.makeDiceBots)], "Choose the type of bots")
    for color in ["blue", "red", "black"]:
        botTeams.append(botsFactory(color))

    tour = Tour([humanTeam] + botTeams)
    tracks = [ randomPresetTrack for i in range(racesCount) ]

    allDisplays = displayRegistry.getAll()
    runner = Runner(window, clock, allDisplays)
    runner.runTour(tour, tracks)

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

def createPlayerOracle(root, window):
    oracle = UserChoice(window)
    def onExit(oracle):
        oracle.dontWait()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", partial(onExit, oracle))
    return oracle

def pickRiders(window):
    number = createSimpleMenu(window, [1, 2, 3, 4], "How many riders in your team?")
    return [ createMenu(window, [ (rider.name, rider) for rider in [ rouleurSpecialist(), sprinteurSpecialist(), grimpeurSpecialist(), opportunisticSpecialist() ]], "Add a rider to your team") for i in range(number) ]


if __name__ == "__main__":
    main()

