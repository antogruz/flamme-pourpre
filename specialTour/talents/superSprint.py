from talent import Talent
from jeu.energyRules import EnergyRules

class SuperSprint(Talent):
    def applyTo(self, personnage):
        personnage.energyRules = SuperSprintEnergyRules(personnage.energyRules)

    def displayRule(self):
        return "Super Sprint: Vos 9 font 11"

class SuperSprintEnergyRules(EnergyRules):
    def __init__(self, base):
        self.base = base

    def energyFromMove(self, move):
        if move.label()[0] == '9':
            return move.energy() + 2
        return self.base.energyFromMove(move)
