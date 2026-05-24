#!/usr/bin/env python3

# Tests d'intégration UI-agnostiques.
#
# Reproduisent les scénarios historiques (bots dice, peloton standard,
# 2 courses opportunistic) en passant par UserInterface, comme une vraie
# partie. Lancer avec --ui pour cibler une implémentation d'UI.

import argparse

import launcher
from engineRunner import EngineRunner
from jeu.tour import Tour
from jeu.tracks import randomPresetTrack
from jeu.teamBuilder import TeamBuilder
from jeu.propulsion import SimpleTeamPropulsion
from oracle import DefaultOracle


def integrationTests(ui):
    def runAll():
        testDice(ui)
        integrationSingle(ui)
        twoRacesOpportunistic(ui)
    ui.run(runAll)


def testDice(ui):
    displays = ui.displays()
    animations = ui.animations(displays)
    runner = EngineRunner(displays, animations)
    botsDirector = ui.botsTeamsDirector()
    teams = [botsDirector.makeDiceBots(color) for color in ["blue", "red", "black"]]
    runner.runRace(randomPresetTrack(len(teams)), teams)


def integrationSingle(ui):
    displays = ui.displays()
    animations = ui.animations(displays)
    runner = EngineRunner(displays, animations)
    botsDirector = ui.botsTeamsDirector()
    teams = [botsDirector.makeStandardBots(color)
             for color in ["green", "red", "blue", "black", "magenta"]]
    runner.runRace(randomPresetTrack(len(teams)), teams)


def twoRacesOpportunistic(ui):
    displays = ui.displays()
    colors = ["blue", "red", "black"]
    director = ui.playerRidersDirector(len(colors), displays)
    oracle = DefaultOracle()
    teams = []
    for color in colors:
        tb = TeamBuilder()
        tb.buildPropulsion(SimpleTeamPropulsion())
        tb.addRider(director.makeOpportunistic(oracle, color))
        teams.append(tb.getResult())
    tour = Tour(teams)
    animations = ui.animations(displays)
    runner = EngineRunner(displays, animations)
    runner.runTour(tour, [randomPresetTrack, randomPresetTrack])


def main():
    parser = argparse.ArgumentParser(description="Integration tests")
    parser.add_argument("--ui", default="tk", choices=sorted(launcher.UIS.keys()))
    args = parser.parse_args()
    ui = launcher.UIS[args.ui](fast=True)
    integrationTests(ui)


if __name__ == "__main__":
    main()
