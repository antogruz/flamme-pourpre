#! /usr/bin/env python3

from decorators.riderDisplay import rouleurShade, sprinteurShade, grimpeurShade, opportunisticShade
from jeu.riderBuilder import RiderBuilder
from jeu.riderMove import MovementRules
from jeu.dicePropulsor import DicePropulsor
from jeu.drawOnePropulsor import DrawOnePropulsor
from specialTour.profiles.personnagesProfiles import rouleurStandardProfile, sprinteurStandardProfile

class RidersDirector:
    def __init__(self, builder = RiderBuilder()):
        self.builder = builder

    def makeRouleur(self, oracle, color):
        builder = self.builder
        builder.buildMovementRules(MovementRules())
        builder.buildAppearance("Rouleur", rouleurShade, color)
        builder.buildOracle(oracle)
        builder.buildDeck(rouleurDeck())
        rider = builder.getResult()
        rider.profile = rouleurStandardProfile()
        return rider

    def makeSprinteur(self, oracle, color):
        builder = self.builder
        builder.buildMovementRules(MovementRules())
        builder.buildAppearance("Sprinteur", sprinteurShade, color)
        builder.buildOracle(oracle)
        builder.buildDeck(sprinteurDeck())
        rider = builder.getResult()
        rider.profile = sprinteurStandardProfile()
        return rider

    def makeGrimpeur(self, oracle, color):
        builder = self.builder
        builder.buildMovementRules(MovementRules())
        builder.buildAppearance("Grimpeur", grimpeurShade, color)
        builder.buildOracle(oracle)
        builder.buildDeck(grimpeurDeck())
        return builder.getResult()

    def makeOpportunistic(self, oracle, color, sets = ["goldenrod", "magenta"]):
        builder = self.builder
        builder.buildMovementRules(MovementRules())
        builder.buildAppearance("Opportunistic", opportunisticShade, color)
        builder.buildOracle(oracle)
        builder.buildOpportunisticDeck([2, 3, 4, 5, 9], sets)
        return builder.getResult()

    def makeDiceRider(self, color):
        builder = self.builder
        builder.buildMovementRules(MovementRules())
        builder.buildAppearance("Rouleur", rouleurShade, color)
        builder.buildPropulsor(DicePropulsor([3, 4, 5, 6, 7, 8]))
        return builder.getResult()

    def makeDiceSprinteur(self, color):
        builder = self.builder
        builder.buildMovementRules(MovementRules())
        builder.buildAppearance("Sprinteur", sprinteurShade, color)
        builder.buildPropulsor(DicePropulsor([2, 3, 4, 5, 6, 10]))
        return builder.getResult()

    def makeMuscleRouleur(self, color):
        builder = self.builder
        builder.buildMovementRules(MovementRules())
        builder.buildAppearance("Rouleur", rouleurShade, color)
        builder.buildPropulsor(DrawOnePropulsor(rouleurDeck()))
        return builder.getResult()

    def makeMuscleSprinteur(self, color):
        builder = self.builder
        builder.buildMovementRules(MovementRules())
        builder.buildAppearance("Sprinteur", sprinteurShade, color)
        builder.buildPropulsor(DrawOnePropulsor(sprinteurDeck() + [5]))
        return builder.getResult()

def rouleurDeck():
    return threeTimes([3, 4, 5, 6, 7])

def sprinteurDeck():
    return threeTimes([2, 3, 4, 5, 9])

def grimpeurDeck():
    return [3, 3, 4, 4, 5, 5, 5, 5, 5, 5, 5, 6, 6, 7, 7]

def threeTimes(five):
    return [ card for card in five for i in range(3) ]
