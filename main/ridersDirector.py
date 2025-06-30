#! /usr/bin/env python3

from decorators.riderDisplay import rouleurShade, sprinteurShade, grimpeurShade, opportunisticShade
from jeu.riderBuilder import RiderBuilder
from jeu.riderMove import MovementRules
from jeu.dicePropulsor import DicePropulsor

class RidersDirector:
    def __init__(self, builder = RiderBuilder()):
        self.builder = builder

    def makeRouleur(self, oracle):
        builder = self.builder
        builder.buildMovementRules(MovementRules())
        builder.buildTexts(rouleurShade, "Rouleur")
        builder.buildOracle(oracle)
        builder.buildDeck(rouleurDeck())
        return builder.getResult()

    def makeSprinteur(self, oracle):
        builder = self.builder
        builder.buildMovementRules(MovementRules())
        builder.buildTexts(sprinteurShade, "Sprinteur")
        builder.buildOracle(oracle)
        builder.buildDeck(sprinteurDeck())
        return builder.getResult()

    def makeGrimpeur(self, oracle):
        builder = self.builder
        builder.buildMovementRules(MovementRules())
        builder.buildTexts(grimpeurShade, "Grimpeur")
        builder.buildOracle(oracle)
        builder.buildDeck(grimpeurDeck())
        return builder.getResult()

    def makeOpportunistic(self, oracle, sets = ["goldenrod", "magenta"]):
        builder = self.builder
        builder.buildMovementRules(MovementRules())
        builder.buildTexts(opportunisticShade, "Opportunistic")
        builder.buildOracle(oracle)
        builder.buildOpportunisticDeck([2, 3, 4, 5, 9], sets)
        return builder.getResult()

    def makeDiceRider(self):
        builder = self.builder
        builder.buildMovementRules(MovementRules())
        builder.buildTexts(rouleurShade, "Rouleur")
        builder.buildPropulsor(DicePropulsor([3, 4, 5, 6, 7, 8]))
        return builder.getResult()

    def makeDiceSprinteur(self):
        builder = self.builder
        builder.buildMovementRules(MovementRules())
        builder.buildTexts(sprinteurShade, "Sprinteur")
        builder.buildPropulsor(DicePropulsor([2, 3, 4, 5, 6, 10]))
        return builder.getResult()


def rouleurDeck():
    return threeTimes([3, 4, 5, 6, 7])

def sprinteurDeck():
    return threeTimes([2, 3, 4, 5, 9])

def grimpeurDeck():
    return [3, 3, 4, 4, 5, 5, 5, 5, 5, 5, 5, 6, 6, 7, 7]

def threeTimes(five):
    return [ card for card in five for i in range(3) ]
