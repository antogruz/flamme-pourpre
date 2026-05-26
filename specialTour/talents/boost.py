from talent import Talent
from deckPropulsor import CombiningChoice, BoostedCard


class Boost(Talent):
    def __init__(self, bonus = 2, uses = 1):
        self.bonus = bonus
        self.uses = uses

    def applyTo(self, personnage):
        personnage.propulsor.addExtraChoice(BoostChoice(self.bonus, self.uses))

    def displayRule(self):
        return f"Boost : {self.uses} fois par course, ajoutez {self.bonus} à l'énergie d'une carte jouée."


class BoostChoice(CombiningChoice):
    def __init__(self, bonus, uses):
        self.bonus = bonus
        self.uses = uses
        self.remainingUses = uses

    def label(self):
        return f"Boost +{self.bonus}"

    def isAvailable(self):
        return self.remainingUses > 0

    def combine(self, move, propulsor):
        self.remainingUses -= 1
        return BoostedCard(move, self.bonus)

    def newRace(self):
        self.remainingUses = self.uses
