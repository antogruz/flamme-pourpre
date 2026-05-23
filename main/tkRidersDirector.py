#!/usr/bin/env python3

# Façade UI Tk autour de RidersDirector. Pour chaque type de coureur,
# paramètre le builder avec son apparence (name + shade ASCII + color Tk)
# avant de déléguer la construction au directeur métier. C'est ensuite
# RiderBuilderWithAppearance.getResult() qui register l'apparence dans
# le registre Appearances consommé par les displays Tk.
#
# Une UI alternative (Pygame, papercraft, etc.) écrira sa propre façade
# équivalente avec ses propres types d'apparence.

from decorators.riderDisplay import rouleurShade, sprinteurShade, grimpeurShade, opportunisticShade


class TkRidersDirector:
    def __init__(self, base, appearances):
        self.base = base
        self.appearances = appearances

    def makeRouleur(self, oracle, color):
        self.base.builder.buildAppearance("Rouleur", rouleurShade, color)
        return self.base.makeRouleur(oracle)

    def makeSprinteur(self, oracle, color):
        self.base.builder.buildAppearance("Sprinteur", sprinteurShade, color)
        return self.base.makeSprinteur(oracle)

    def makeGrimpeur(self, oracle, color):
        self.base.builder.buildAppearance("Grimpeur", grimpeurShade, color)
        return self.base.makeGrimpeur(oracle)

    def makeOpportunistic(self, oracle, color, sets = ["goldenrod", "magenta"]):
        self.base.builder.buildAppearance("Opportunistic", opportunisticShade, color)
        return self.base.makeOpportunistic(oracle, sets)

    def makeDiceRider(self, color):
        self.base.builder.buildAppearance("Rouleur", rouleurShade, color)
        return self.base.makeDiceRider()

    def makeDiceSprinteur(self, color):
        self.base.builder.buildAppearance("Sprinteur", sprinteurShade, color)
        return self.base.makeDiceSprinteur()

    def makeMuscleRouleur(self, color):
        self.base.builder.buildAppearance("Rouleur", rouleurShade, color)
        return self.base.makeMuscleRouleur()

    def makeMuscleSprinteur(self, color):
        self.base.builder.buildAppearance("Sprinteur", sprinteurShade, color)
        return self.base.makeMuscleSprinteur()
