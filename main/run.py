#!/usr/bin/env python3

import tkinter as tk
from tracks import *
from menu import *
from runner import Runner
from tour import Tour
from cardsDisplay import CardsDisplay
from teamBuilder import TeamBuilder
from ridersDirector import RidersDirector
from teamsDirector import TeamsDirector, FirstOracle
from opportunisticDisplay import OpportunisticDisplay
from propulsion import SequentialPropulsion

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
    director = RidersDirector()
    specialDisplayers = []
    for i in range(ridersCount):
        riderType = createSimpleMenu(window, ["Rouleur", "Sprinteur", "Grimpeur", "Opportunistic"], "Add a rider to your team")
        if riderType == "Rouleur":
            rider = director.makeRouleur(oracle)
        elif riderType == "Sprinteur":
            rider = director.makeSprinteur(oracle)
        elif riderType == "Grimpeur":
            rider = director.makeGrimpeur(oracle)
        elif riderType == "Opportunistic":
            sets = ["goldenrod", "magenta"]
            rider = director.makeOpportunistic(oracle, sets)
            specialDisplayers.append(OpportunisticDisplay(playerLayout.ridersSpecialFrames[i], [sorted([ card for card in rider.propulsor.cards.deck if color in str(card)]) for color in sets], rider.propulsor.cards))
        tb.addRider(rider)
    humanTeam = tb.getResult()
    teamsDirector = TeamsDirector()
    botTeams = []
    botsFactory = createMenu(window, [("Standard", teamsDirector.makeStandardBots), ("Dice", teamsDirector.makeDiceBots)], "Choose the type of bots")
    for color in ["blue", "red", "black"]:
        botTeams.append(botsFactory(color))

    cardsDisplayers = [ CardsDisplay(riderFrame, rider) for rider, riderFrame in zip(humanTeam.riders, playerLayout.ridersCards) ]
    tour = Tour([humanTeam] + botTeams)
    tracks = [ randomPresetTrack for i in range(racesCount) ]
    runner = Runner(window, clock, cardsDisplayers + specialDisplayers)
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

