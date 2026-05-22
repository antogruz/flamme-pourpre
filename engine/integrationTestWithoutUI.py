#!/usr/bin/env python3

# Test d'intégration headless : prouve que EngineRunner peut faire tourner
# un tour complet de plusieurs courses sans aucune dépendance Tk, en
# utilisant NoopUIBackend. Garantit que le moteur reste décorrélé de l'UI.

from tour import Tour
from tracks import randomPresetTrack
from teamBuilder import TeamBuilder
from propulsion import SimpleTeamPropulsion
from dicePropulsor import DicePropulsor
from personnage import Personnage
from riderMove import MovementRules
from energyRules import EnergyRules
from engineRunner import EngineRunner
from uiBackend import NoopUIBackend


def makeBotTeam():
    tb = TeamBuilder()
    tb.buildPropulsion(SimpleTeamPropulsion())
    tb.addRider(makeDiceRider())
    tb.addRider(makeDiceRider())
    return tb.getResult()


def makeDiceRider():
    return Personnage(MovementRules(), DicePropulsor([3, 4, 5, 6, 7, 8]), EnergyRules())


def main():
    teams = [makeBotTeam() for _ in range(3)]
    tour = Tour(teams)
    runner = EngineRunner(NoopUIBackend())
    runner.runTour(tour, [randomPresetTrack, randomPresetTrack])
    scores = tour.getScores()
    assert len(scores) == len(teams), "Expected one score per team"
    print("integrationTestWithoutUI: OK -", len(scores), "teams scored")


if __name__ == "__main__":
    main()
