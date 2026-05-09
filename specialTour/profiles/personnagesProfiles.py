from specialTour.talents.effortLong import EffortLong
from specialTour.talents.economieEnergie import EconomieEnergie
from specialTour.talents.endurance import Endurance
from specialTour.talents.poursuivant import Poursuivant
from specialTour.talents.echappe import Echappe
from specialTour.talents.rouleRoule import RouleRoule
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
