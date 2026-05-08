#! /usr/bin/env python3


class EffortLong:
    def applyTo(self, personnage):
        personnage.energyRules = BetterFatigue(personnage.energyRules, 3)


class BetterFatigue:
    def __init__(self, base, fatigueValue):
        self.base = base
        self.fatigueValue = fatigueValue

    def energyFromCard(self, card):
        if card == "f":
            return self.fatigueValue
        return self.base.energyFromCard(card)
