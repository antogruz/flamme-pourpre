#! /usr/bin/env python3

from talent import Talent


class EffortLong(Talent):
    def applyTo(self, personnage):
        personnage.energyRules = BetterFatigue(personnage.energyRules, 3)

    def displayRule(self):
        return "Effort prolongé: Les cartes fatigue font 3"


class BetterFatigue:
    def __init__(self, base, fatigueValue):
        self.base = base
        self.fatigueValue = fatigueValue

    def energyFromMove(self, move):
        if move.label()[0] == "f":
            return self.fatigueValue
        return self.base.energyFromMove(move)
