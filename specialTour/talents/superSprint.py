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

    def energyFromCard(self, card):
        if card == 9:
            return 11
        return self.base.energyFromCard(card)