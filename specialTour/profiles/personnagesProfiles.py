from effortLong import EffortLong
from economieEnergie import EconomieEnergie
from endurance import Endurance
from poursuivant import Poursuivant
from echappe import Echappe
from rouleRoule import RouleRoule
class PersonnageProfile:
    def __init__(self, name, tiers):
        self.name = name
        self.tiers = tiers
        self.currentTier = 0

    def getAccessibleTalents(self):
        return self.tiers[self.currentTier]

    def nextTier(self):
        self.currentTier += 1


def rouleurStandardProfile():
    return PersonnageProfile("Rouleur Standard",
    tiers = [
        [EffortLong, EconomieEnergie, Endurance],
        [Poursuivant, Echappe, RouleRoule]
    ])
