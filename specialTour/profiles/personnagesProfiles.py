from specialTour.talents.effortLong import EffortLong
from specialTour.talents.economieEnergie import EconomieEnergie
from specialTour.talents.endurance import Endurance
from specialTour.talents.poursuivant import Poursuivant
from specialTour.talents.echappe import Echappe
from specialTour.talents.rouleRoule import RouleRoule
from specialTour.talents.remonteeDePeloton import RemonteeDePeloton
from specialTour.talents.inlarguable import Inlarguable
from specialTour.talents.seFaufiler import SeFaufiler
from specialTour.talents.superSprint import SuperSprint
from specialTour.talents.sprintFinal import SprintFinal
from specialTour.talents.recuperationActive import RecuperationActive
from specialTour.talents.regularite import Regularite
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

def sprinteurStandardProfile():
    return PersonnageProfile("Sprinteur Standard",
    tiers = [
        [RemonteeDePeloton, Inlarguable, SeFaufiler],
        [SuperSprint, SprintFinal, RecuperationActive, Regularite]
    ])