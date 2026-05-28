#! /usr/bin/env python3

# Directeur métier : construit des Personnages typés (rouleur, sprinteur,
# grimpeur, opportuniste, bots) avec deck, propulsor, profile.
# Ne touche pas à l'apparence visuelle : c'est la responsabilité des
# façades UI (cf. homeMadeUI/tkRidersDirector.py pour l'UI Tk).
#
# Chaque makeXxx crée un RiderBuilder neuf : aucun état n'est partagé
# entre deux coureurs successifs construits par le même director (sinon
# self.energyRules et autres attributs sticky du builder pourraient
# fuiter d'un coureur à l'autre).
#
# Vit dans main/ et non dans jeu/ uniquement parce que les profiles
# référencent les talents de specialTour/ (qui dépend de jeu/) : le mettre
# dans jeu/ introduirait jeu/ → specialTour/.

from jeu.riderBuilder import RiderBuilder
from jeu.riderMove import StandardMovementRules
from jeu.dicePropulsor import DicePropulsor
from jeu.drawOnePropulsor import DrawOnePropulsor
from specialTour.profiles.personnagesProfiles import rouleurStandardProfile, sprinteurStandardProfile

class RidersDirector:
    def makeRouleur(self, oracle):
        builder = RiderBuilder()
        builder.buildMovementRules(StandardMovementRules())
        builder.buildOracle(oracle)
        builder.buildDeck(rouleurDeck())
        rider = builder.getResult()
        rider.profile = rouleurStandardProfile()
        return rider

    def makeSprinteur(self, oracle):
        builder = RiderBuilder()
        builder.buildMovementRules(StandardMovementRules())
        builder.buildOracle(oracle)
        builder.buildDeck(sprinteurDeck())
        rider = builder.getResult()
        rider.profile = sprinteurStandardProfile()
        return rider

    def makeGrimpeur(self, oracle):
        builder = RiderBuilder()
        builder.buildMovementRules(StandardMovementRules())
        builder.buildOracle(oracle)
        builder.buildDeck(grimpeurDeck())
        return builder.getResult()

    def makeOpportunistic(self, oracle, sets = ["goldenrod", "magenta"]):
        builder = RiderBuilder()
        builder.buildMovementRules(StandardMovementRules())
        builder.buildOracle(oracle)
        builder.buildOpportunisticDeck([2, 3, 4, 5, 9], sets)
        return builder.getResult()

    def makeDiceRider(self):
        builder = RiderBuilder()
        builder.buildMovementRules(StandardMovementRules())
        builder.buildPropulsor(DicePropulsor([3, 4, 5, 6, 7, 8]))
        return builder.getResult()

    def makeDiceSprinteur(self):
        builder = RiderBuilder()
        builder.buildMovementRules(StandardMovementRules())
        builder.buildPropulsor(DicePropulsor([2, 3, 4, 5, 6, 10]))
        return builder.getResult()

    def makeMuscleRouleur(self):
        builder = RiderBuilder()
        builder.buildMovementRules(StandardMovementRules())
        builder.buildPropulsor(DrawOnePropulsor(rouleurDeck()))
        return builder.getResult()

    def makeMuscleSprinteur(self):
        builder = RiderBuilder()
        builder.buildMovementRules(StandardMovementRules())
        builder.buildPropulsor(DrawOnePropulsor(sprinteurDeck() + [5]))
        return builder.getResult()

def rouleurDeck():
    return threeTimes([3, 4, 5, 6, 7])

def sprinteurDeck():
    return threeTimes([2, 3, 4, 5, 9])

def grimpeurDeck():
    return [3, 3, 4, 4, 5, 5, 5, 5, 5, 5, 5, 6, 6, 7, 7]

def threeTimes(five):
    return [card for card in five for i in range(3)]
