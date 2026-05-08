#! /usr/bin/env python3

class EconomieEnergie:
    def applyTo(self, personnage):
        personnage.energyRules = BetterEmpty(personnage.energyRules, 3)
        personnage.propulsor.addExtraChoice(SkipProvider())


class BetterEmpty:
    def __init__(self, base, emptyValue):
        self.base = base
        self.emptyValue = emptyValue

    def energyFromCard(self, card):
        if card == "":
            return self.emptyValue
        return self.base.energyFromCard(card)


class SkipProvider:
    def label(self):
        return ""

    def isAvailable(self):
        return True

    def applyTo(self, propulsor):
        propulsor.cards.discardHand()
